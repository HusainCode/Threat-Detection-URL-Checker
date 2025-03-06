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
import httpx
import os  # Provides functions to interact
# with the operating system, including environment variables
from dotenv import load_dotenv  # Loads environment variables from a .env file
from pathlib import Path  # Handles file system paths in a cross-platform way
from google.cloud import webrisk_v1
from google.cloud.webrisk_v1 import SearchUrisResponse
from google.oauth2 import service_account
from src.csv_handler import CVSHandler
import asyncio
import json
import csv
import aiohttp
import time

# Loads API key securely from .env file
load_dotenv(Path(__file__).resolve().parent / ".env")

# Set Google credentials
CREDENTIALS_PATH = os.environ["GOOGLE_APPLICATION_CREDENTIALS"]
API_KEY = os.getenv("GOOGLE_API_KEY")

class APIHandler:
    CURRENT_LIMIT = 5 # API rate limits to prevent overloading

    def __init__(self):
        self.API_SOURCE = (f"https://webrisk.googleapis.com/v1/uris:search?key={API_KEY} \
                            &uri=https://theaxolotlapi.netlify.app/,Animals")

        """
          According to the doc there are the only threat typs the API can check
          Threat typs to test against:
          1- ThreatType.MALWARE
          2- ThreatType.SOCIAL_ENGINEERING
          3- ThreatType.UNWANTED_SOFTWARE
          4- ThreatType.SOCIAL_ENGINEERING_EXTENDED_COVERAGE
         """
        valid_threats = frozenset([

            webrisk_v1.ThreatType.MALWARE,
            webrisk_v1.ThreatType.SOCIAL_ENGINEERING,
            webrisk_v1.ThreatType.UNWANTED_SOFTWARE,
            webrisk_v1.ThreatType.SOCIAL_ENGINEERING_EXTENDED_COVERAGE,
        ])
        self.THREAT_TYPE = frozenset(threat for threat in valid_threats)

        self.credentials = service_account.Credentials.from_service_account_file(
            "key.json"
        )

        self.CVSHandler = CVSHandler()


    async def fetching_API_data(self) -> str:
        '''
        Sends an asynchronous GET request to the Google webrisk API

        :param URL: The API endpoint to fetch the data from

        :return: JSON response, if error is detected, return the error
        '''

        # Send a GET request to the server
        async with httpx.AsyncClient() as client:
            response = await client.get(self.API_SOURCE, timeout=5.0) # timeout is 5 for now, adjust later
            response.raise_for_status() # raise http error, example: 4xx/5xx

            success_responses = 200  # Define success condition

            if response.status_code == success_responses:
                try:
                    return response.json()  # Convert response to JSON
                except json.JSONDecodeError:
                    print("Error: Response is not valid JSON")
                except (httpx.TimeoutException, httpx.ConnectError) as e:
                    print(f"Network error: {e}")
                except httpx.HTTPStatusError as e:
                  # Examples:
                  # 404 Not Found (wrong URL)
                  # 500 Internal Server Error (server issue)
                  # 403 Forbidden (you don’t have permission)
                  print(f"Http Error: {response.status_code}:{e}")
                except httpx.RequestError as e:
                    print(f"Request failed: {e}")


                    # I STOPPED HERE
                    # NEEDS TO ASYNC


    # Source: https://cloud.google.com/web-risk/docs/lookup-api#python


def search_uri(self, api: str) -> SearchUrisResponse:
    """Checks whether a URI is on a given threatList.

        Multiple threatLists may be searched in a single query. The response will list all
        requested threatLists the URI was found to match. If the URI is not
        found on any of the requested ThreatList an empty response will be returned.

        Args:
            uri: The URI to be checked for matches
                Example: "http://testsafebrowsing.appspot.com/s/malware.html"

        Returns:
            SearchUrisResponse that contains a threat_type if the URI is present in the threatList.
        """

    # Initialize web risk client
    # Creat a connection to the Google API
    webrisk_client = webrisk_v1.WebRiskServiceClient(credentials=self.credentials)

    request = webrisk_v1.SearchUrisRequest()  # Specify the type of threat
    request.threat_types = self.THREAT_TYPE
    request.uri = api

    response = webrisk_client.search_uris(request)
    if response.threat.threat_types:
        print(f"This API is not safe! It has the following threat:{response}")
    else:
        print(f"This API is safe!")
    return response

    # process the coming APIs list


async def worker(self,  API):
    pass




API = APIHandler()
asyncio.run(API.fetching_API_data())
# API.search_uri("https://theaxolotlapi.netlify.app/,Animals")
