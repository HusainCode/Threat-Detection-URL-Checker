# ThreatAnalyzer is responsible
#
#  Purpose:
#
#  Key Attributes:
#
#
#  Main Methods:
#
import pandas as pd
import matplotlib.pyplot as plt

class ThreatAnalyzer:
    def __init__(self, results_file="results.csv"):
        self.results_file = results_file

    def load_results(self):
        try:
            return pd.read_csv(self.results_file)
        except FileNotFoundError:
            print("No results file found.")
            return None

    def generate_tables(self):
        """Generates a table from results.csv"""
        data = self.load_results()
        if data is None:
            return

        print("\nThreat Analysis Report")
        print(data)

    def generate_charts(self):
        """Generates a bar chart showing the threat type distribution"""
        data = self.load_results()
        if data is None:
            return

        counts = data["Threat Type"].value_counts()

        plt.figure(figsize=(8, 5))
        counts.plot(kind="bar", color=["green", "red", "orange", "blue"])
        plt.title("Threat Analysis Results")
        plt.xlabel("Threat Type")
        plt.ylabel("Count")
        plt.xticks(rotation=45)
        plt.grid(axis="y", linestyle="--", alpha=0.7)

        plt.savefig("threat_analysis_chart.png")
        plt.show()
