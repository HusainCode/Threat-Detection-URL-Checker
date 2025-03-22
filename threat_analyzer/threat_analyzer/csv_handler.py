# Purpose:
#   Handle CSV input/output operations including loading API links,
#   saving results, and calculating threat percentages.
#
# Key Attributes:
#   csv_path: Path to the input CSV file (from .env)
#   results_file: Path to the results output CSV (from .env)
#
# Main Methods:
#   load_API_link()
#  save_results_to_csv(results)
#   get_percentage()

import csv
import os
from collections import Counter

import os

import os

class CSVHandler:
    def __init__(self):
        base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))

        self.csv_path = os.path.join(base_dir, os.getenv("CSV_FILE"))
        self.results_file = os.path.join(base_dir, os.getenv("RESULTS_FILE"))

        # Optional: print paths for debugging
        print(f"[DEBUG] CSV path: {self.csv_path}")
        print(f"[DEBUG] Results path: {self.results_file}")


    def load_API_link(self) -> list:
        """Loads API links from the CSV file."""
        with open(self.csv_path, newline="", encoding="utf-8") as file:
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

    def get_percentage(self) -> dict:
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




