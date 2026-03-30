
import httpx
from bs4 import BeautifulSoup
import asyncio
from typing import List, Dict, Any, Optional

# Global client for connection pooling (Crucial for latency reduction)
_http_client: Optional[httpx.AsyncClient] = None

def get_http_client() -> httpx.AsyncClient:
    global _http_client
    if _http_client is None:
        limits = httpx.Limits(max_keepalive_connections=10, max_connections=20)
        _http_client = httpx.AsyncClient(limits=limits, follow_redirects=True)
    return _http_client

EXCHANGE_URLS = {
    "binance": "https://www.binance.com/en/support/announcement/c-48?navId=48",
    "kucoin": "https://www.kucoin.com/news/categories/listing",
    "bybit": "https://announcements.bybit.com/en-US/?category=new_crypto",
    "gateio": "https://www.gate.io/articlelist/ann"
}

LISTING_KEYWORDS = ["launchpool"]

async def scrape_exchange_announcements() -> List[Dict[str, Any]]:
    client = get_http_client()
    # Run all requests in parallel using the shared connection pool
    tasks = [fetch_and_parse(client, exchange, url) for exchange, url in EXCHANGE_URLS.items()]
    results = await asyncio.gather(*tasks)
    
    all_announcements = []
    for result in results:
        if result:
            all_announcements.extend(result)
            
    return all_announcements

async def fetch_and_parse(client: httpx.AsyncClient, exchange: str, url: str) -> Optional[List[Dict[str, Any]]]:
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        # Connection is reused, significantly reducing request time
        response = await client.get(url, headers=headers, timeout=5.0)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'html.parser')
        announcements = []
        
        links = soup.find_all('a')
        for link in links:
            text = link.get_text().lower()
            href = link.get('href')

            if any(keyword in text for keyword in LISTING_KEYWORDS):
                if href and not href.startswith('javascript'):
                    full_url = href if href.startswith('http') else f"https://www.binance.com{href}"
                    announcements.append({
                        "source": exchange,
                        "title": link.get_text().strip(),
                        "url": full_url,
                        "timestamp_detected": asyncio.get_event_loop().time()
                    })
        return announcements

    except httpx.HTTPStatusError as e:
        return None
    except Exception as e:
        return None

