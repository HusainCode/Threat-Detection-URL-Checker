#  Purpose:
#     Acts as the entry point of the application. It loads environment variables,
#     initializes components (logger, CSV handler, API handler, analyzer), and
#     orchestrates the full flow of the URL threat analysis process.
#
#  Key Attributes:
#     CREDENTIALS_PATH: Path to the Google service account JSON
#     API_KEY: Google API key used for requests
#     PUBLIC_APIs_LIST: Path to input CSV containing URLs to scan
#
#  Main Functions:
#     main(): Async function that controls the high-level workflow
#
#  Example:
#     Run the script:
#         python main.py
#
#     Output:
#         Processing your request.....
#         Process completed successfully.
#         The program took: [X.XX] seconds


import asyncio
from threat_analyzer.api_handler import APIHandler
from threat_analyzer.csv_handler import CSVHandler
from threat_analyzer.logger import Logger
from threat_analyzer.threat_analyzer import ThreatAnalyzer
import time

from dotenv import load_dotenv
import os

# Load .env variables once
load_dotenv()

# Retrieve environment variables
CREDENTIALS_PATH = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
API_KEY = os.getenv("GOOGLE_API_KEY")
PUBLIC_APIs_LIST = os.getenv("CSV_FILE")

async def main():
    # Initialize components
    logger = Logger()
    csv_handler = CSVHandler()
    api_handler = APIHandler()
    threat_analyzer = ThreatAnalyzer()

    # Fetch URLs from CSV
    urls = csv_handler.load_API_link()
    if not urls:
        logger.error("No URLs found in CSV file.")
        return

    # Pass data to APIHandler and process URLs
    logger.info("Starting URL analysis...")
    await api_handler.process_urls()

    # Analyze threats and generate reports
    logger.info("Generating threat analysis reports...")
    threat_analyzer.generate_charts()

    logger.info("Process completed successfully.")

if __name__ == "__main__":
    start = time.perf_counter()

    print("Processing your request.....")
    asyncio.run(main())

    print("\nProcess completed successfully.")

    end = time.perf_counter()
    print(f"The program took: {end - start:.2f} seconds")


# Run full-app profiling and save results:
# python -m cProfile -o profile_output.prof threat_analyzer/main.py
# Visualize with:
# snakeviz profile_output.prof
