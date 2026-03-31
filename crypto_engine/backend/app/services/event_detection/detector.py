
import time
import re
import dateparser
from typing import Dict, Any, Optional, Tuple

# Regex to find potential crypto tickers (e.g., (BTC), (ETH))
# It looks for 2-6 uppercase letters inside parentheses.
TICKER_REGEX = re.compile(r'\(([A-Z]{2,6})\)')

# Keywords to classify the event type
EVENT_TYPE_KEYWORDS = {
    "Launchpool": ["launchpool"],
}

def parse_raw_announcement(announcement: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """
    Parses a raw announcement dictionary to extract structured event data.
    Only allows Launchpool events.
    """
    title = announcement.get('title', '').lower()
    
    # 1. Determine Event Type FIRST to filter early
    event_type = determine_event_type(title)
    if event_type != "Launchpool":
        return None

    # 2. Extract Token Symbol
    token_symbol = extract_token_symbol(announcement.get('title', '')) # Use original title for regex
    if not token_symbol:
        return None

    # 3. Extract Listing Time (This is a simplified example)
    listing_time = extract_listing_time(announcement.get('title', '') + announcement.get('body', ''))

    # 4. Construct the structured event
    det_ts = announcement.get('timestamp_detected')
    if det_ts is None:
        det_ts = announcement.get('timestamp')
    if det_ts is None:
        det_ts = time.time()

    structured_event = {
        "event_type": event_type,
        "token_symbol": token_symbol,
        "exchange": announcement.get('source'),
        "announcement_url": announcement.get('url'),
        "detection_timestamp": det_ts,
        "listing_timestamp": listing_time.timestamp() if listing_time else None,
        "hype_score": calculate_hype_score(title)
    }
    
    return structured_event

def extract_token_symbol(text: str) -> Optional[str]:
    """Extracts a cryptocurrency ticker symbol from text using regex or keywords."""
    # 1. Try parenthesized ticker (e.g., (BTC))
    match = TICKER_REGEX.search(text.upper()) 
    if match:
        return match.group(1)
    
    # 2. Try common Launchpool formats like "Stake BASED" or "Earn MNT"
    words = text.upper().split()
    for i, word in enumerate(words):
        if word in ["STAKE", "EARN", "LIST", "LAUNCHPOOL"] and i + 1 < len(words):
            potential_ticker = words[i+1].strip('.,():')
            # Filter out common non-ticker words
            if potential_ticker not in ["SHARE", "A", "POTENTIAL", "NEW", "TOKENS", "SHARE", "POOL", "REWARDS"]:
                if 2 <= len(potential_ticker) <= 6 and potential_ticker.isalpha():
                    return potential_ticker
                
    return None

def determine_event_type(text: str) -> Optional[str]:
    """Determines the event type based on keywords in the text. Returns None if not Launchpool."""
    for event, keywords in EVENT_TYPE_KEYWORDS.items():
        if any(keyword in text for keyword in keywords):
            return event
    return None

def extract_listing_time(text: str) -> Optional[object]:
    """Parses a human-readable date/time string from the text."""
    try:
        match = re.search(r'(\d{4}-\d{2}-\d{2}\s\d{2}:\d{2})\sUTC', text)
        if match:
            return dateparser.parse(match.group(1))
        return None
    except Exception:
        return None

def calculate_hype_score(text: str) -> int:
    """Calculates a basic hype score. Placeholder logic."""
    score = 1
    if "fully diluted" in text: score += 1
    if "megadrop" in text: score += 2
    return score

