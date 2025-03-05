# CVSHandler is responsible for loading API data from a CSV file.
#
#  Purpose:
# - Reads a CSV file path from a hidden `.env` file
# - Extracts API URLs and descriptions from the CSV
#
#  Key Attributes:
#  self.PUBLIC_APIs_LIST stores the file path of the CSV
#
#  Main Methods:
# 1.  __prepare_file_path() Loads the CSV file path from `.env`
# 2. load_API_link() Extracts API links from the CSV
# 3. load_description() Extracts API descriptions from the CSV

import csv
import os
from dotenv import load_dotenv


class CVSHandler:
    def __init__(self):
        self.__prepare_file_path()

    # load the path from the '.env' hidden file
    def __prepare_file_path(self) -> None:
        load_dotenv()
        self.PUBLIC_APIs_LIST = os.getenv("CSV_FILE")

    # load the API links
    # Example: https://theaxolotlapi.netlify.app/
    def load_API_link(self) -> list:
        with open(self.PUBLIC_APIs_LIST, newline="", encoding="utf-8") as links_file:
            links = csv.DictReader(links_file)
            url = [row['Link'] for row in links]  # store links in a list
            return url

    # Loads APIs descriptions
    # Example: Collection of axolotl pictures and facts
    def load_description(self) -> list:
        with open(self.PUBLIC_APIs_LIST, newline="", encoding="utf-8") as descriptions_file:
            descriptions = csv.DictReader(descriptions_file)
            description = [row["Description"] for row in descriptions]
            return description



# h1 = CVSHandler()
#
# print(h1.load_description())
# print("\n",h1.load_API_link())
