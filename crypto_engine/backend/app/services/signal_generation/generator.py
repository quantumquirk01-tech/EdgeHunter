
import time
import math
from typing import Dict, Any, Optional

from app.core.config import settings
from app.services.execution.exchanges.base import Exchange

# --- Dynamic Scoring Weights ---
BASE_WEIGHTS = {
    "major_exchange": {"binance": 5, "bybit": 4, "kucoin": 3, "gateio": 2, "default": 1},
    "liquidity_baseline": 3,
    "social_velocity": 2, 
}

ENTER_THRESHOLD = 8.0
WATCH_THRESHOLD = 5.0

def calculate_time_decay(age_seconds: float) -> float:
    """Exponential time decay: The edge disappears rapidly after announcement."""
    # After 5 seconds, score drops significantly.
    decay_factor = math.exp(-0.2 * age_seconds) 
    return max(0, 5 * decay_factor) # Max 5 points for speed

def validate_liquidity_and_spread(market_context: Dict[str, Any]) -> bool:
    """Crucial Edge: Ignore fake liquidity and massive spreads."""
    spread = market_context.get('spread_percentage', 100)
    liquidity = market_context.get('liquidity_usd', 0)
    
    # Reject if spread is > 5% at launch (prevents buying the extreme top)
    if spread > 5.0:
        print(f"WARN: Spread too high ({spread}%). Rejecting signal.")
        return False
        
    # Reject if liquidity is suspiciously low for a major exchange
    if liquidity < 10000:
        print(f"WARN: Liquidity too low (${liquidity}). Potential honeypot/fake. Rejecting.")
        return False
        
    return True

async def generate_signal_from_event(event: Dict[str, Any], exchange_client: Optional[Exchange] = None) -> Optional[Dict[str, Any]]:
    time_since_detection = time.time() - event['detection_timestamp']
    
    if time_since_detection > settings.SIGNAL_MAX_EVENT_AGE_SECONDS:
        return None

    # If no exchange client (no API keys), use mock market context to show the signal
    if exchange_client is None:
        market_context = {
            "is_tradable": True,
            "liquidity_usd": 50000.0,
            "spread_percentage": 0.5,
            "orderbook_imbalance": 2.0,
            "current_price": 0.0
        }
    else:
        market_context = await exchange_client.get_market_context(event['token_symbol'])
        if not market_context['is_tradable'] or not validate_liquidity_and_spread(market_context):
            return None

    score = 0
    
    # 1. Base Exchange Score
    score += BASE_WEIGHTS["major_exchange"].get(event['exchange'], BASE_WEIGHTS["major_exchange"]["default"])

    # 2. Advanced Alpha: Exponential Time Decay Score
    score += calculate_time_decay(time_since_detection)

    # 3. Dynamic Imbalance Score (Non-linear)
    imbalance = market_context.get('orderbook_imbalance', 1.0)
    if imbalance > 3.0:
        score += 4 # Massive buy pressure
    elif imbalance > 1.5:
        score += 2 # Moderate buy pressure
    elif imbalance < 0.8:
        score -= 3 # Sell pressure at launch (Bad sign)

    if score >= ENTER_THRESHOLD:
        decision = "ENTER"
    elif score >= WATCH_THRESHOLD:
        decision = "WATCH"
    else:
        decision = "IGNORE"

    if decision == "IGNORE":
        return None

    signal = {
        "decision": decision,
        "score": round(score, 2),
        "token_symbol": event['token_symbol'],
        "exchange": event['exchange'],
        "event_type": event['event_type'],
        "announcement_url": event['announcement_url'],
        "signal_timestamp": time.time(),
        "market_context": market_context,
        "metrics": {
            "decay_applied": calculate_time_decay(time_since_detection),
            "latency_sec": time_since_detection
        }
    }
    
    return signal

