import unittest
import os
import csv
import tempfile
from unittest.mock import patch
from threat_analyzer.csv_handler import CSVHandler


class TestCSVHandler(unittest.TestCase):
    def setUp(self):
        # Create temporary CSV files for testing
        self.input_file = tempfile.NamedTemporaryFile(mode='w+', delete=False, newline='', suffix='.csv')
        self.results_file = tempfile.NamedTemporaryFile(delete=False, suffix='.csv')
        self.results_file.close()  # close immediately to prevent window lock

        # Write sample input CSV for load_API_link
        writer = csv.DictWriter(self.input_file, fieldnames=["Link"])
        writer.writeheader()
        writer.writerow({"Link": "https://example.com"})
        writer.writerow({"Link": "https://malware.com"})
        self.input_file.close()

        # Patch environment variables to point to temp files
        patcher = patch.dict(os.environ, {
            "CSV_FILE": self.input_file.name,
            "RESULTS_FILE": self.results_file.name
        })
        self.addCleanup(patcher.stop)
        patcher.start()

        self.handler = CSVHandler()

    def tearDown(self):
        # Cleanup temp files
        os.unlink(self.input_file.name)
        os.unlink(self.results_file.name)

    def test_csv_paths_are_set(self):
        self.assertTrue(self.handler.csv_path.endswith(".csv"))
        self.assertTrue(self.handler.results_file.endswith(".csv"))

    def test_load_API_link(self):
        links = self.handler.load_API_link()
        self.assertEqual(len(links), 2)
        self.assertIn("https://example.com", links)
        self.assertIn("https://malware.com", links)

    def test_save_results_to_csv(self):
        test_data = {
            "https://example.com": "SAFE",
            "https://malware.com": "MALWARE"
        }
        self.handler.save_results_to_csv(test_data)

        with open(self.results_file.name, newline='', encoding='utf-8') as f:
            reader = csv.reader(f)
            rows = list(reader)
            self.assertEqual(len(rows), 3)  # header + 2 rows
            self.assertIn(["https://example.com", "SAFE"], rows)
            self.assertIn(["https://malware.com", "MALWARE"], rows)

    def test_get_percentage(self):
        # Prepare fake results CSV
        # Open the fake results file in write mode
        with open(self.results_file.name, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f) # this method takes a file object, returns a writer object
            # Write a header just like a real CSV file

            writer.writerow(["URL", "Threat Type"])
            writer.writerow(["https://site1.com", "SAFE"])
            writer.writerow(["https://site2.com", "MALWARE"])
            writer.writerow(["https://site3.com", "MALWARE"])

        result = self.handler.get_percentage()
        self.assertAlmostEqual(result["SAFE"], 33.33, delta=0.1)
        self.assertAlmostEqual(result["MALWARE"], 66.66, delta=0.1)


if __name__ == "__main__":
    unittest.main()
