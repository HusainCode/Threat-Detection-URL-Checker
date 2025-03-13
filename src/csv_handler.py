import csv
import os
from dotenv import load_dotenv

class CVSHandler:
    def __init__(self):
        self.__prepare_file_path()

    def __prepare_file_path(self) -> None:
        load_dotenv()
        self.PUBLIC_APIs_LIST = os.getenv("CSV_FILE")

    def load_API_link(self) -> list:
        """Loads API links from the CSV file."""
        with open(self.PUBLIC_APIs_LIST, newline="", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            return [row["Link"] for row in reader]

    def save_results_to_csv(self, results: dict):
        """Saves URL scan results to a CSV file."""
        results_file = "results.csv"

        with open(results_file, 'a', newline='', encoding="utf-8") as file:
            writer = csv.writer(file)

            if file.tell() == 0:
                writer.writerow(["URL", "Threat Type"])

            for url, threat in results.items():
                writer.writerow([url, threat])
