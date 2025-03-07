# # Process of Fetching an API
# # 1️ Send a request → Connect to the API using GET.
# # 2 Receives a response → API returns data (JSON, XML, CSV, etc.).
# # 3 Parse the response → Convert data into a usable format.
# # 4 Extract URLs → Filter out relevant URLs from the data.
# # 5️ Use the URLs → Pass them to your checker for processing
#
# APIHandler is responsible
#
#  Purpose:
#
#  Key Attributes:
#
#
#  Main Methods:
#
import queue
import httpx
import os  # Provides functions to interact with the operating system, including environment variables
from dotenv import load_dotenv  # Loads environment variables from a .env file
from pathlib import Path  # Handles file system paths in a cross-platform way

from google.cloud import webrisk_v1
from google.cloud.webrisk_v1 import (
    SearchUrisResponse,
    SearchUrisRequest,
    WebRiskServiceClient,

)
from google.api_core.exceptions import (
    InvalidArgument,
    PermissionDenied,
    NotFound,
    InternalServerError,
)

from google.oauth2 import service_account
from src.csv_handler import CVSHandler
import asyncio

import tracemalloc

import json
import csv
import aiohttp
import time

tracemalloc.start()

# Loads API key securely from .env file
load_dotenv(Path(__file__).resolve().parent / ".env")

# Set Google credentials
CREDENTIALS_PATH = os.environ["GOOGLE_APPLICATION_CREDENTIALS"]
API_KEY = os.getenv("GOOGLE_API_KEY")


class APIHandler:
    CURRENT_LIMIT = 5  # API rate limits to prevent overloading

    def __init__(self):
        self.API_SOURCE = (
            f"https://webrisk.googleapis.com/v1/uris:search?key={API_KEY}&uri=https://theaxolotlapi.netlify.app/,Animals"
        )

        """
        source: https://cloud.google.com/web-risk/docs/reference/rest/v1/ThreatType
        
        ThreatType:
        The type of threat. This maps directly to the threat list a threat may belong to.
        
        1- THREAT_TYPE_UNSPECIFIED:
        	       No entries should match this threat type. This threat type is unused.
        2- MALWARE:	
                   Malware targeting any platform.
        3- SOCIAL_ENGINEERING:	
                    Social engineering targeting any platform.
        4- UNWANTED_SOFTWARE:	
                     Unwanted software targeting any platform.
        5- SOCIAL_ENGINEERING_EXTENDED_COVERAGE:	
                      A list of extended coverage social engineering URIs targeting any platform.
        
        """
        valid_threats = frozenset(
            [
                webrisk_v1.ThreatType.MALWARE,
                webrisk_v1.ThreatType.SOCIAL_ENGINEERING,
                webrisk_v1.ThreatType.UNWANTED_SOFTWARE,
                webrisk_v1.ThreatType.SOCIAL_ENGINEERING_EXTENDED_COVERAGE,
            ]
        )
        self.THREAT_TYPE = [threat for threat in valid_threats]

        self.credentials = service_account.Credentials.from_service_account_file(
            "key.json"
        )

        self.CVSHandler = CVSHandler()
        self.queue = asyncio.Queue()

        # Initialize web risk client
        # Create a connection to the Google API
        self.webrisk_client = WebRiskServiceClient(credentials=self.credentials)

        self.semaphore = asyncio.Semaphore(APIHandler.CURRENT_LIMIT) # current limit is 5


    # Source: https://cloud.google.com/web-risk/docs/lookup-api#python
    async def search_uri(self, uri: str) -> SearchUrisResponse:
        """
        Checks whether a URI is on a given threatList.
        Sends an asynchronous GET request to the Google webrisk API

        Multiple threatLists may be searched in a single query. The response will list all
        requested threatLists the URI was found to match. If the URI is not
        found on any of the requested ThreatList an empty response will be returned.

        Args:
            uri: The URI to be checked for matches
                Example: "https://testsafebrowsing.appspot.com/s/malware.html"

        Param URL: The API endpoint to fetch the data from

        Returns:
            SearchUrisResponse that contains a threat_type if the URI is present in the threatList.
            If error is detected, return the error

             """

        # Google Web Risk API only allows ONE URL per request
        loop = asyncio.events.get_running_loop()

        request = SearchUrisRequest()  # Specify the type of threat
        request.threat_types = self.THREAT_TYPE
        request.uri = uri

        response = self.webrisk_client.search_uris(request)

        try:

            response = await asyncio.to_thread(self.webrisk_client.search_uris, request)

            if response.threat.threat_types:
                print(f"This API is not safe! It has the following threat: {response}")
            else:
                print(f"This API is safe!")
            return response

        except InvalidArgument as e:
            print(f"Invalid argument: {e.message}")
        except PermissionDenied as e:
            print(f"Permission denied: {e.message}")
        except NotFound as e:
            print(f"Not found: {e.message}")
        except InternalServerError as e:
            print(f"Internal server error: {e.message}")

    # Process the coming APIs list
    async def worker(self, api):
        await self.queue.put(api)

        async with self.semaphore:
            url = await self.queue.get()
            await self.search_uri(url)
            self.queue.task_done()  # Mark the task as done


    # def logger_messanger(self):
    #     pass


# API = APIHandler()
#
# asyncio.create_task(API.worker("https://theaxolotlapi.netlify.app/,Animals"))


# API.search_uri("https://theaxolotlapi.netlify.app/,Animals")

# snapshot = tracemalloc.take_snapshot()
# top_stats = snapshot.statistics("lineno")

