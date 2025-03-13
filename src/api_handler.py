import os
import asyncio
from dotenv import load_dotenv
from google.cloud import webrisk_v1
from google.oauth2 import service_account
from google.api_core.exceptions import InvalidArgument, PermissionDenied, NotFound, InternalServerError

from src.csv_handler import CVSHandler
from src.logger import Logger

load_dotenv()

CREDENTIALS_PATH = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
API_KEY = os.getenv("GOOGLE_API_KEY")

class APIHandler:
    CURRENT_LIMIT = 5  # API rate limit

    def __init__(self):
        self.THREAT_TYPE = [
            webrisk_v1.ThreatType.MALWARE,
            webrisk_v1.ThreatType.SOCIAL_ENGINEERING,
            webrisk_v1.ThreatType.UNWANTED_SOFTWARE,
            webrisk_v1.ThreatType.SOCIAL_ENGINEERING_EXTENDED_COVERAGE,
        ]

        self.credentials = service_account.Credentials.from_service_account_file("key.json")
        self.webrisk_client = webrisk_v1.WebRiskServiceClient(credentials=self.credentials)
        self.csv_handler = CVSHandler()
        self.logger = Logger()

        self.queue = asyncio.Queue()
        self.semaphore = asyncio.Semaphore(APIHandler.CURRENT_LIMIT)

    async def search_uri(self, uri: str) -> str:
        request = webrisk_v1.SearchUrisRequest(uri=uri, threat_types=self.THREAT_TYPE)

        try:
            response = await asyncio.to_thread(self.webrisk_client.search_uris, request)

            if response.threat.threat_types:
                self.logger.warning(f"Threat detected on {uri}: {response.threat.threat_types}")
                return response.threat.threat_types[0].name
            else:
                self.logger.info(f"{uri} is safe.")
                return "SAFE"

        except (InvalidArgument, PermissionDenied, NotFound, InternalServerError) as e:
            self.logger.error(f"Error checking {uri}: {str(e)}")
            return "ERROR"

    async def worker(self):
        while not self.queue.empty():
            async with self.semaphore:
                url = await self.queue.get()
                threat_type = await self.search_uri(url)
                self.queue.task_done()
                return url, threat_type

    async def process_urls(self):
        urls = self.csv_handler.load_API_link()
        for url in urls:
            await self.queue.put(url)

        workers = [asyncio.create_task(self.worker()) for _ in range(APIHandler.CURRENT_LIMIT)]
        results = await asyncio.gather(*workers)

        self.csv_handler.save_results_to_csv(dict(results))
