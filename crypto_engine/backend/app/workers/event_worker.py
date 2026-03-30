
import asyncio
import json
from redis.asyncio import Redis

from app.services.event_detection.detector import parse_raw_announcement
from app.core.config import settings

async def event_detection_worker():
    """
    A continuous worker that consumes raw announcements from one Redis queue,
    parses them into structured events, and pushes them to another queue
    for the Signal Engine.
    """
    redis_client = Redis.from_url(settings.REDIS_URL, decode_responses=True)
    print("INFO: Event Detection Worker started.")

    while True:
        try:
            # Blocking pop from the raw_events queue (with a timeout)
            # This is efficient as it doesn't poll unnecessarily.
            raw_event_json = await redis_client.brpop(settings.REDIS_RAW_EVENTS_QUEUE, timeout=0)

            if raw_event_json:
                # brpop returns a tuple (queue_name, item)
                _, raw_event_data = raw_event_json
                raw_announcement = json.loads(raw_event_data)
                
                print(f"INFO: Processing raw event: {raw_announcement.get('title')}")

                # The core parsing logic
                structured_event = parse_raw_announcement(raw_announcement)

                if structured_event:
                    # If parsing is successful, push the structured event to the next queue
                    await redis_client.lpush(
                        settings.REDIS_PARSED_EVENTS_QUEUE,
                        json.dumps(structured_event)
                    )
                    print(f"SUCCESS: Parsed event and queued for signal generation: {structured_event}")
                else:
                    print(f"WARN: Failed to parse raw event, discarding: {raw_announcement.get('title')}")

        except asyncio.CancelledError:
            print("INFO: Event Detection Worker shutting down.")
            break
        except Exception as e:
            print(f"CRITICAL: Event Detection Worker crashed: {e}")
            # Avoid rapid-fire crashes
            await asyncio.sleep(30)

