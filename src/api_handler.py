# # Process of Fetching an API
# # 1️ Send a request → Connect to the API using GET.
# # 2 Receive a response → API returns data (JSON, XML, CSV, etc.).
# # 3 Parse the response → Convert data into a usable format.
# # 4 Extract URLs → Filter out relevant URLs from the data.
# # 5️ Use the URLs → Pass them to your checker for processing
#
import requests
import os  #Provides functions to interact
           # with the operating system, including environment variables
from dotenv import load_dotenv # Loads environment variables from a .env file
from pathlib import Path # Handles file system paths in a cross-platform way
from google.cloud import webrisk_v1
from google.cloud.webrisk_v1 import SearchUrisResponse


class APIHandler:

    def __init__(self):

        self.API_KEY = self.__prepare_API()
        self.API_SOURCE = (f"https://webrisk.googleapis.com/v1/uris:search?key={self.API_KEY} \
                            &uri=https://theaxolotlapi.netlify.app/,Animals")

        """
          1- Threat typs to test against 
          2- ThreatType.THREAT_TYPE_UNSPECIFIED
          3- ThreatType.MALWARE
          4- ThreatType.SOCIAL_ENGINEERING
          5- ThreatType.UNWANTED_SOFTWARE
          6- ThreatType.SOCIAL_ENGINEERING_EXTENDED_COVERAGE
         """
        self.THREAT_TYPE = frozenset(threat for threat in webrisk_v1.ThreatType)

    def __prepare_API(self):
        # Loads API key securely from .env file
        load_dotenv(Path(__file__).resolve().parent / ".env")
        # Set Google credentials
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
        return os.getenv("GOOGLE_API_KEY")

    def fetching_API_data(self):
        response = requests.get(self.API_SOURCE)

        # First, check if response is valid before calling .json()
        if response.status_code == 200 and response.text.strip():
            try:
                return response.json()  # Convert response to JSON
            except requests.exceptions.JSONDecodeError:
                print("Error: Response is not valid JSON")
                return None
        else:
            print(f"Error: {response.status_code}")
            return None

    # Source: https://cloud.google.com/web-risk/docs/lookup-api#python
    def search_uri(self,api: str) -> SearchUrisResponse:
        """Checks whether a URI is on a given threatList.

            Multiple threatLists may be searched in a single query. The response will list all
            requested threatLists the URI was found to match. If the URI is not
            found on any of the requested ThreatList an empty response will be returned.

            Args:
                uri: The URI to be checked for matches
                    Example: "http://testsafebrowsing.appspot.com/s/malware.html"
                threat_type: The ThreatLists to search in. Multiple ThreatLists may be specified.
                    Example: threat_type = webrisk_v1.ThreatType.MALWARE

            Returns:
                SearchUrisResponse that contains a threat_type if the URI is present in the threatList.
            """

        # Initialize web risk client
        # Creat a connection to the Google API
        webrisk_client = webrisk_v1.WebRiskServiceClient()

        request = webrisk_v1.SearchUrisRequest()  # Specify the type of threat
        request.threat_types = self.THREAT_TYPE
        request.uri = api

        response = webrisk_client.search_uris(request)
        if response.threat.threat_types:
            print(f"This API is not safe! It has the following threat:{response}")
        else:
            print(f"This API is safe!")
        return response





API = APIHandler()
API.search_uri("https://theaxolotlapi.netlify.app/,Animals")



