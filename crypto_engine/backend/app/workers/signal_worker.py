
import asyncio
import json
from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.db.base import AsyncSessionLocal
from app.services.signal_generation.generator import generate_signal_from_event
from app.services.risk_management.manager import assess_risk_and_create_order
from app.services.notification.telegram_bot import send_telegram_notification

# This is a conceptual import. The client factory will be built as part of the Execution Engine.
from app.services.execution.executor import get_exchange_client

async def signal_processing_worker():
    """
    A continuous worker that consumes structured events, generates signals,
    and passes them to the risk and execution engines.
    """
    redis_client = Redis.from_url(settings.REDIS_URL, decode_responses=True)
    print("INFO: Signal Processing Worker started.")

    while True:
        try:
            # Blocking pop from the parsed_events queue
            _, event_data = await redis_client.brpop(settings.REDIS_PARSED_EVENTS_QUEUE, timeout=0)
            event = json.loads(event_data)
            
            print(f"INFO: Processing parsed event for signal generation: {event['token_symbol']}")

            # Get the appropriate exchange client for the event
            exchange_client = get_exchange_client(event['exchange'])
            if not exchange_client:
                print(f"WARN: No exchange client found for {event['exchange']}. Proceeding with signal generation anyway.")

            # Generate the signal using the core alpha logic
            signal = await generate_signal_from_event(event, exchange_client)

            if signal:
                # If a valid signal (ENTER or WATCH) is generated, send a notification
                await send_telegram_notification(signal)

                # If the decision is to ENTER, proceed to risk management
                if signal['decision'] == "ENTER":
                    async with AsyncSessionLocal() as db:
                        order_to_execute = await assess_risk_and_create_order(db, signal)
                    
                    if order_to_execute:
                        print(f"INFO: Risk assessment passed. Pushing order to execution queue for {signal['token_symbol']}")
                        # In a real system, this would go to another Redis queue for the execution engine.
                        # For simplicity here, we'll call the executor directly.
                        from app.services.execution.executor import execute_order
                        await execute_order(order_to_execute)
                    else:
                        print(f"INFO: Signal for {signal['token_symbol']} rejected by Risk Management Engine.")

        except asyncio.CancelledError:
            print("INFO: Signal Processing Worker shutting down.")
            break
        except Exception as e:
            print(f"CRITICAL: Signal Processing Worker crashed: {e}")
            await asyncio.sleep(30)

