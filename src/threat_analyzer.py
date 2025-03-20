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
from src.csv_handler import CVSHandler

class ThreatAnalyzer:
    def __init__(self, results_file="results.csv"):
        self.results_file = results_file
        self.colors = [ "green", "red", "blue", "orange"]
        self.labels = ["SAFE", "MALWARE", "SOCIAL_ENGINEERING", "UNWANTED_SOFTWARE"]

        self.csv_handler = CVSHandler()

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
        """Generates a pie chart showing the threat type distribution"""
        data = self.load_results()
        if data is None:
            return

        counts = data["Threat Type"].value_counts()

        plt.figure(figsize=(20, 15))  #
        wedges, texts, autotexts = plt.pie(
            counts.values, labels=counts.index, colors=self.colors, autopct="%1.1f%%",
            startangle=140, pctdistance=0.85, labeldistance=1.1
        )


        for text in texts:
            text.set_fontsize(10)
        for autotext in autotexts:
            autotext.set_fontsize(10)

        plt.legend(counts.index, loc="best", fontsize=10)
        plt.title("Threat Type Distribution Results", fontsize=14, pad=20)
        plt.savefig("threat_distribution_results.png", bbox_inches="tight")
        plt.show()


