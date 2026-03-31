
import asyncio
import time
from typing import List, Dict
from unittest.mock import MagicMock

from app.services.signal_generation.generator import generate_signal_from_event
from app.services.risk_management.manager import assess_risk_and_create_order

# Mock Exchange Client for Backtesting
class MockExchange:
    def __init__(self, mock_market_data):
        self.mock_market_data = mock_market_data
        
    async def get_market_context(self, symbol: str):
        return self.mock_market_data.get(symbol, {"is_tradable": False})

async def run_backtest(historical_events: List[Dict], mock_market_data: Dict):
    print("\n" + "="*50)
    print("🚀 STARTING BACKTEST SIMULATION 🚀")
    print("="*50)
    
    exchange_client = MockExchange(mock_market_data)
    results = {"total_trades": 0, "approved": 0, "rejected": 0, "simulated_pnl": 0}
    mock_db = MagicMock()

    for event in historical_events:
        print(f"\n--- Simulating Event: {event['token_symbol']} on {event['exchange']} ---")
        
        # 1. Signal Generation
        signal = await generate_signal_from_event(event, exchange_client)
        if not signal:
            print("❌ Signal Engine: IGNORED (Score too low or failed validation)")
            continue
            
        print(f"✅ Signal Engine: {signal['decision']} (Score: {signal['score']})")
        
        if signal['decision'] == "ENTER":
            # 2. Risk Management
            order = await assess_risk_and_create_order(mock_db, signal)
            if not order:
                print("❌ Risk Engine: REJECTED")
                results["rejected"] += 1
            else:
                print(f"✅ Risk Engine: APPROVED. Order Type: {order['order_type']}, Size: ${order['position_size_usd']:.2f}")
                results["approved"] += 1
                results["total_trades"] += 1
                
                # Simulate Outcome (Simplified)
                if order['order_type'] == "LIMIT_IOC":
                    print("   Outcome: Executed safely with minimal slippage. Win.")
                    results["simulated_pnl"] += (order['position_size_usd'] * 0.20) # Simulate hitting TP1
                else:
                    print("   Outcome: Executed via MARKET. Slipped heavily. Loss.")
                    results["simulated_pnl"] -= (order['position_size_usd'] * 0.08) # Simulate hitting SL

    print("\n" + "="*50)
    print("📊 BACKTEST RESULTS 📊")
    print(f"Total Signals Processed: {len(historical_events)}")
    print(f"Trades Executed: {results['approved']}")
    print(f"Trades Rejected by Risk: {results['rejected']}")
    print(f"Estimated Net PnL: ${results['simulated_pnl']:.2f}")
    print("="*50 + "\n")

# --- Sample Data ---
if __name__ == "__main__":
    now = time.time()
    
    sample_events = [
        {
            "event_type": "New Listing", "token_symbol": "GOOD_COIN", "exchange": "binance",
            "announcement_url": "url", "detection_timestamp": now - 1 # 1 second delay (Fast)
        },
        {
            "event_type": "New Listing", "token_symbol": "BAD_COIN", "exchange": "binance",
            "announcement_url": "url", "detection_timestamp": now - 10 # 10 seconds delay (Slow)
        },
        {
            "event_type": "New Listing", "token_symbol": "SCAM_COIN", "exchange": "kucoin",
            "announcement_url": "url", "detection_timestamp": now - 2 
        }
    ]
    
    sample_market_data = {
        "GOOD_COIN": {"is_tradable": True, "current_price": 1.0, "liquidity_usd": 500000, "spread_percentage": 0.5, "orderbook_imbalance": 4.0}, # Perfect setup
        "BAD_COIN": {"is_tradable": True, "current_price": 1.0, "liquidity_usd": 100000, "spread_percentage": 1.5, "orderbook_imbalance": 1.0}, # Slow, average
        "SCAM_COIN": {"is_tradable": True, "current_price": 1.0, "liquidity_usd": 5000, "spread_percentage": 15.0, "orderbook_imbalance": 0.5}, # Fake liquidity, massive spread
    }

    asyncio.run(run_backtest(sample_events, sample_market_data))
