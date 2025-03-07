import asyncio
from src.api_handler import APIHandler

async def main():
    API = APIHandler()  # Initialize the API handler

    # List of URLs to check 
    urls = [
        "https://theaxolotlapi.netlify.app/,Animals",
    ]

    # Create a list of async tasks for URL checking
    tasks = [asyncio.create_task(API.worker(url)) for url in urls]

    # Wait for all tasks to complete
    await asyncio.gather(*tasks)

if __name__ == "__main__":
    asyncio.run(main())
