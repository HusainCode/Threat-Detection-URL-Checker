#  Purpose:
#     Handles the interaction with Google's Web Risk API to analyze URLs
#     for potential threats such as malware or phishing.
#
#  Key Attributes:
#     THREAT_TYPE: List of threat types checked against the API
#     credentials: Google service account credentials
#     webrisk_client: WebRisk API client
#     csv_handler: Handles input/output CSV operations
#     logger: Logs events, results, and errors
#     queue: Async queue for URLs
#     semaphore: Limits concurrent API requests
#
#  Main Methods:
#     search_uri(uri): Asynchronously checks a URL against Google Web Risk
#     worker(): Async worker that pulls from the queue and processes a URL
#     process_urls(): Loads URLs from CSV, creates workers, and stores results


import os # Provides functions to interact with the operating system, including environment variables
import asyncio # Provides async functionalities
from dotenv import load_dotenv # Loads environment variables from a .env file
from google.cloud import webrisk_v1
from google.oauth2 import service_account
from google.api_core.exceptions import InvalidArgument, PermissionDenied, NotFound, InternalServerError

from threat_analyzer.csv_handler import CSVHandler
from threat_analyzer.logger import Logger

# Loads variables from .env
load_dotenv()

# Retrieve values from the environment variables
CREDENTIALS_PATH = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
API_KEY = os.getenv("GOOGLE_API_KEY")

class APIHandler:

    def __init__(self):
        """
        source: https://cloud.google.com/web-risk/docs/reference/rest/v1/ThreatType

        ThreatType:
        The type of threat. This maps directly to the threat list a threat may belong to.

        1. THREAT_TYPE_UNSPECIFIED
        No entries should match this threat type. This threat type is unused.

        2. MALWARE (webrisk_v1.ThreatType.MALWARE)
        Unwanted software targeting any platform.

        3. SOCIAL_ENGINEERING (webrisk_v1.ThreatType.SOCIAL_ENGINEERING)
        Deceptive sites that trick users into doing something dangerous, such as revealing passwords.

        4. UNWANTED_SOFTWARE (webrisk_v1.ThreatType.UNWANTED_SOFTWARE)
        Software that may negatively impact the user experience without being explicitly malicious.

        5. SOCIAL_ENGINEERING_EXTENDED_COVERAGE (webrisk_v1.ThreatType.SOCIAL_ENGINEERING_EXTENDED_COVERAGE)
        A list of extended coverage social engineering URIs targeting any platform.
       """
        self.THREAT_TYPE = [
            webrisk_v1.ThreatType.MALWARE,
            webrisk_v1.ThreatType.SOCIAL_ENGINEERING,
            webrisk_v1.ThreatType.UNWANTED_SOFTWARE,
            webrisk_v1.ThreatType.SOCIAL_ENGINEERING_EXTENDED_COVERAGE,
        ]

        self.api_key = os.getenv("GOOGLE_API_KEY")


        # This is essential to process requests.
        # The Google API provides the key.json credentials to process requests.
        # Loads Google service account credentials form the json file to authenticate API access.
        self.credentials = service_account.Credentials.from_service_account_file("../resources/key.json")

        # Create clint object
        # This part is essential to interact with the Google Web Risk API
        # You must first initialize the client before using any of the Google Web Risk API features
        self.webrisk_client = webrisk_v1.WebRiskServiceClient(credentials=self.credentials)

        self.csv_handler = CSVHandler()
        self.logger = Logger()

        self.queue = asyncio.Queue()
        self.semaphore = asyncio.Semaphore()

    async def search_uri(self, uri: str) -> str | list:
        # Sending a request, Google verifies the credentials before processing the request
        request = webrisk_v1.SearchUrisRequest(uri=uri, threat_types=self.THREAT_TYPE)

        try:
            # asyncio.to_thread(func → The blocking function to run in a thread,
            #                   *args → Any arguments to pass to func.)
            # runs a blocking  function in a separate  thread
            # The repsonce will be SearchUrisResponse object.
            # If It's empty, that means it's safe, else threat was detected, and it should return the threat type
            response = await asyncio.to_thread(self.webrisk_client.search_uris, request)

            if response.threat.threat_types: # if threat was detected
                self.logger.warning(f"Threat detected on {uri}: {response.threat.threat_types}")
                return [threat.name for threat in response.threat.threat_types]
            else:
                self.logger.info(f"{uri} is safe.")
                return "SAFE"

        except (InvalidArgument, PermissionDenied, NotFound, InternalServerError) as e:
            self.logger.error(f"Error checking {uri}: {str(e)}")
            return "ERROR"

    # Process the coming APIs list
    async def worker(self):
        while not self.queue.empty():
            async with self.semaphore:
                url = await self.queue.get()
                threat_type = await self.search_uri(url)
                self.queue.task_done() # Mark as done
                return url, threat_type

    async def process_urls(self):
        urls = self.csv_handler.load_API_link()
        for url in urls:
            await self.queue.put(url)

        workers = [asyncio.create_task(self.worker()) for _ in urls]
        results = await asyncio.gather(*workers)

        self.csv_handler.save_results_to_csv(dict(results))

    @property
    def get_threat_types(self) -> list:
        return  self.THREAT_TYPE
