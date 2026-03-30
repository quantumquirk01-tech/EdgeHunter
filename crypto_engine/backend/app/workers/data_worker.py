
import asyncio
import json
from redis.asyncio import Redis

from app.services.data_ingestion.scrapers import scrape_exchange_announcements
from app.services.data_ingestion.coingecko import get_new_listings_coingecko
from app.core.config import settings

# In-memory cache to store URLs of announcements we've already processed
# to prevent sending duplicate events to the queue.
PROCESSED_URLS_CACHE = set()

async def data_ingestion_worker():
    """
    A continuous worker that polls data sources and pushes raw findings
    into a Redis queue for the Event Detection Engine to process.
    """
    redis_client = Redis.from_url(settings.REDIS_URL, decode_responses=True)
    print("INFO: Data Ingestion Worker started.")

    while True:
        try:
            # Primary source: Fast, direct scraping
            scraped_announcements = await scrape_exchange_announcements()
            
            for announcement in scraped_announcements:
                # Deduplication check before pushing to queue
                if announcement['url'] not in PROCESSED_URLS_CACHE:
                    PROCESSED_URLS_CACHE.add(announcement['url'])
                    
                    # Push raw data to the 'raw_events' queue
                    await redis_client.lpush(
                        settings.REDIS_RAW_EVENTS_QUEUE,
                        json.dumps(announcement)
                    )
                    print(f"INFO: Pushed new raw event to queue: {announcement['title']}")

            # Secondary source: Enrichment data (runs less frequently)
            # coingecko_listings = await get_new_listings_coingecko()
            # for listing in coingecko_listings:
            #     # Similar deduplication and queuing logic would go here
            #     pass

            # The polling interval is critical.
            # Too short -> IP bans. Too long -> missed opportunities.
            # Reduced to 3 seconds for Edge
            await asyncio.sleep(3)

        except Exception as e:
            print(f"CRITICAL: Data Ingestion Worker crashed: {e}")
            # Implement a backoff strategy before restarting
            await asyncio.sleep(60) # Wait a minute before retrying

