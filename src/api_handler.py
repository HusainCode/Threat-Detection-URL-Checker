# # rocess of Fetching an API
# # 1️ Send a request → Connect to the API using GET.
# # 2 Receive a response → API returns data (JSON, XML, CSV, etc.).
# # 3 Parse the response → Convert data into a usable format.
# # 4 Extract URLs → Filter out relevant URLs from the data.
# # 5️ Use the URLs → Pass them to your checker for processing
#
import requests

class APIHandler:

    def __init__(self):
        self.API_SOURCE = "https://public-apis.io/api-list"

    def fetching_API_data(self):
        response = requests.get(self.API_SOURCE)
        data = response.json()
        return data

API =APIHandler()

hi = API.fetching_API_data()
print(hi)


