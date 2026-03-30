
import httpx
import json
import asyncio
from typing import Dict, Any

from app.core.config import settings

async def send_telegram_notification(signal: Dict[str, Any]):
    """
    Formats a message from a signal and sends it to a specified Telegram chat.
    Also broadcasts the signal to all connected WebSocket clients.
    """
    # 1. Broadcast via WebSocket
    try:
        from app.main import manager
        # Signal needs to match the frontend 'Signal' type
        current_time_ms = int(asyncio.get_event_loop().time() * 1000)
        frontend_signal = {
            "id": str(current_time_ms),
            "token": signal['token_symbol'],
            "exchange": signal['exchange'].capitalize(),
            "eventType": signal['event_type'],
            "eventSummary": signal.get('event_summary', f"فرصة جديدة على {signal['exchange']}"),
            "eventTimestamp": (signal.get('listing_timestamp') or 0) * 1000,
            "score": signal['score'],
            "detectedAt": current_time_ms,
            "decision": signal['decision'],
            "liquidityUsd": signal.get('market_context', {}).get('liquidity_usd', 0),
            "slippage": signal.get('market_context', {}).get('spread_percentage', 0),
            "sparkline": [signal['score']] * 8, # Placeholder
            "momentum": signal.get('hype_score', 1) / 5,
            "isNew": True
        }
        await manager.broadcast(json.dumps(frontend_signal))
        print(f"INFO: Broadcasted signal for {signal['token_symbol']} via WebSocket.")
    except Exception as e:
        print(f"ERROR: Failed to broadcast via WebSocket: {e}")

    # 2. Telegram Notification
    if not settings.TELEGRAM_BOT_TOKEN or settings.TELEGRAM_BOT_TOKEN == "YOUR_TELEGRAM_BOT_TOKEN":
        print("WARN: Telegram bot token not configured. Skipping notification.")
        return
    
    decision_emoji = "✅" if signal['decision'] == "ENTER" else "👀"
    
    message = (
        f"🚀 *فرصة جديدة* {decision_emoji}\n\n"
        f"*العملة:* `{signal['token_symbol']}`\n"
        f"*الحدث:* {signal['event_type']}\n"
        f"*المنصة:* {signal['exchange'].capitalize()}\n"
        f"*التقييم (Score):* `{signal['score']}`\n"
        f"*القرار:* *{signal['decision']}*\n\n"
        f"[رابط الإعلان]({signal['announcement_url']})"
    )

    telegram_api_url = f"https://api.telegram.org/bot{settings.TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": settings.TELEGRAM_CHAT_ID,
        "text": message,
        "parse_mode": "Markdown",
        "disable_web_page_preview": True
    }

    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(telegram_api_url, json=payload)
            if response.status_code == 200:
                print(f"INFO: Successfully sent Telegram notification for {signal['token_symbol']}.")
            else:
                print(f"ERROR: Failed to send Telegram notification. Status: {response.status_code}, Response: {response.text}")
    except Exception as e:
        print(f"CRITICAL: Exception while sending Telegram notification: {e}")

