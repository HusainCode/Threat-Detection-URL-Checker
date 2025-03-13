import asyncio
from src.api_handler import APIHandler
from src.csv_handler import CVSHandler
from src.logger import Logger
from src.threat_analyzer import ThreatAnalyzer

async def main():
    # Initialize components
    logger = Logger()
    csv_handler = CVSHandler()
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
    threat_analyzer.generate_tables()
    threat_analyzer.generate_charts()

    logger.info("Process completed successfully.")

if __name__ == "__main__":
    asyncio.run(main())
