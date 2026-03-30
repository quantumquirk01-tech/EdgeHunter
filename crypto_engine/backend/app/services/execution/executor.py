
from typing import Dict, Any, Optional

from app.core.config import settings
from .exchanges.base import Exchange
from .exchanges.binance import Binance
# Import other exchange clients as they are built
# from .exchanges.bybit import Bybit
# from .exchanges.kucoin import Kucoin
# from .exchanges.gateio import Gateio

# A dictionary to hold initialized exchange clients (singleton pattern)
_exchange_clients: Dict[str, Exchange] = {}

def _initialize_clients():
    """Initializes all supported exchange clients based on the config."""
    print("INFO: Initializing exchange clients...")
    # Initialize Binance
    if settings.BINANCE_API_KEY != "YOUR_BINANCE_API_KEY":
        _exchange_clients["binance"] = Binance(
            api_key=settings.BINANCE_API_KEY,
            api_secret=settings.BINANCE_API_SECRET
        )
    # Add other exchanges here
    # if settings.BYBIT_API_KEY != "YOUR_BYBIT_API_KEY":
    #     _exchange_clients["bybit"] = Bybit(...)

_initialize_clients() # Initialize on module load

def get_exchange_client(exchange_name: str) -> Optional[Exchange]:
    """Factory function to get an initialized exchange client."""
    return _exchange_clients.get(exchange_name.lower())

async def execute_order(order: Dict[str, Any]):
    """
    The main entry point for the execution engine.
    It finds the correct exchange client and calls its execute method.
    """
    exchange_name = order.get("exchange")
    client = get_exchange_client(exchange_name)

    if not client:
        print(f"CRITICAL: Execution failed. No client available for exchange '{exchange_name}'.")
        return

    try:
        result = await client.execute_order(order)
        
        # After execution, the result should be saved to the database.
        # from app.crud.trade import save_trade_result
        # await save_trade_result(result)
        print(f"INFO: Order execution result for {order['token_symbol']} saved.")

    except Exception as e:
        print(f"CRITICAL: Order execution for {order['token_symbol']} on {exchange_name} failed: {e}")
        # Implement retry logic or a kill-switch here if necessary

