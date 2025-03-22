# Purpose:
#   Analyze threat scan results and generate visual charts.
#
# Key Attributes:
#   results_file: Path to the CSV results file
#   chart_path: Path to save the output chart
#
# Main Methods:
#   generate_charts()

import os
import pandas as pd
import matplotlib.pyplot as plt

class ThreatAnalyzer:
    def __init__(self, results_file=None):
        # Resolve absolute base path to the project root
        base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))

        # Load from environment or use passed-in value
        self.results_file = results_file or os.path.join(base_dir, os.getenv("RESULTS_FILE"))
        self.chart_path = os.path.join(base_dir, os.getenv("CHART_FILE", "resources/threat_analysis_chart.png"))

        # Attempt to read the results file
        if os.path.exists(self.results_file):
            try:
                self.load_results = pd.read_csv(self.results_file)
            except pd.errors.ParserError as e:
                print(f"[ERROR] CSV file parsing failed: {e}")
                self.load_results = pd.DataFrame()
        else:
            print(f"[WARNING] Results file not found: {self.results_file}")
            self.load_results = pd.DataFrame()

        self.colors = ["green", "red", "blue", "orange"]
        self.labels = ["SAFE", "MALWARE", "SOCIAL_ENGINEERING", "UNWANTED_SOFTWARE"]

    def generate_charts(self):
        """Generates a pie chart showing the threat type distribution and saves it."""
        data = self.load_results
        if data.empty:
            print("No data available for chart generation.")
            return

        percentages = data["Threat Type"].value_counts(normalize=True) * 100

        plt.pie(percentages, autopct="%1.1f%%", startangle=90)
        plt.title("Threat Type Distribution Results", fontsize=14, pad=20)
        plt.legend(self.labels, title="Threat Type", loc="best")
        plt.axis("equal")
        plt.tight_layout()

        # Save the chart to the resources folder
        plt.savefig(self.chart_path)
        print(f"Chart saved to: {self.chart_path}")
        plt.close()
