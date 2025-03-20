import csv
import os
from collections import Counter
from dotenv import load_dotenv

class CVSHandler:
    def __init__(self):
        self.results_file = "results.csv"
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
        with open(self.results_file, 'w', newline='', encoding="utf-8") as file:
            writer = csv.writer(file)

            if file.tell() == 0:
                writer.writerow(["URL", "Threat Type"])

            for url, threat in results.items():
                writer.writerow([url, threat])

    def get_percentage(self):
        if not self.results_file:
            raise ValueError("Results file is not set. Run save_results_to_csv first")

        results = []  # Store threat types

        with open(self.results_file, mode="r", newline="", encoding="utf-8") as read_file:
            reader = csv.reader(read_file)
            next(reader)  # Skip header row

            for row in reader:
                results.append(row[-1])  # Get the last column (Threat Type)

        total = len(results) if results else 1  # Avoid division by zero
        counts = Counter(results)

        percentage = {threat: (count / total) * 100 for threat, count in counts.items()}
        return percentage




