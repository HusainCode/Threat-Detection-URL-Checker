import unittest
import pandas as pd
import os
import tempfile
from unittest.mock import patch
from threat_analyzer.threat_analyzer import ThreatAnalyzer

class TestThreatAnalyzer(unittest.TestCase):
    def setUp(self):
        # Create a dummy results file path and chart path
        self.results_file = tempfile.NamedTemporaryFile(delete=False, suffix='.csv')
        self.chart_file = tempfile.NamedTemporaryFile(delete=False, suffix='.png')
        self.results_file.close()
        self.chart_file.close()

        # Patch the required env variables manually
        self.env_patcher = patch.dict(os.environ, {
            "RESULTS_FILE": os.path.basename(self.results_file.name),
            "CHART_FILE": os.path.basename(self.chart_file.name)
        })
        self.env_patcher.start()

        # Create dummy .csv with empty data
        with open(self.results_file.name, 'w', encoding='utf-8') as f:
            f.write("Threat Type\n")  # header only

        self.analyzer = ThreatAnalyzer()

    def tearDown(self):
        # Clean up files and environment patch
        os.unlink(self.results_file.name)
        os.unlink(self.chart_file.name)
        self.env_patcher.stop()

    def test_results_file_exists_or_empty(self):
        self.assertIsInstance(self.analyzer.load_results, pd.DataFrame)

    def test_generate_charts_handles_empty(self):
        self.analyzer.load_results = pd.DataFrame()
        self.analyzer.generate_charts()  # Should not raise anything

    def test_labels_and_colors_length(self):
        self.assertEqual(len(self.analyzer.colors), len(self.analyzer.labels))

if __name__ == "__main__":
    unittest.main()
