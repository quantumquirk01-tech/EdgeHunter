
from abc import ABC, abstractmethod
from typing import Dict, Any

class Exchange(ABC):
    """
    An abstract base class defining the standard interface for all exchange clients.
    This ensures that the core logic can interact with any exchange in a uniform way.
    """

    def __init__(self, api_key: str, api_secret: str, passphrase: str = None):
        self.api_key = api_key
        self.api_secret = api_secret
        self.passphrase = passphrase
        self.name = self.__class__.__name__.lower()
        print(f"INFO: Initialized {self.name} exchange client.")

    @abstractmethod
    async def get_market_context(self, symbol: str) -> Dict[str, Any]:
        """
        Fetches live, pre-listing market data for a given symbol.
        This is one of the most critical and difficult parts in a real system.

        Returns a dictionary with keys like:
        - 'is_tradable': bool
        - 'current_price': float (or estimated opening price)
        - 'liquidity_usd': float
        - 'orderbook_imbalance': float (buy_volume / sell_volume)
        - 'spread_percentage': float
        """
        pass

    @abstractmethod
    async def execute_order(self, order: Dict[str, Any]) -> Dict[str, Any]:
        """
        Executes a trade order on the exchange.

        Args:
            order: An order dictionary created by the Risk Management Engine.

        Returns:
            A dictionary containing the result of the execution, e.g., trade ID, status.
        """
        pass

    @abstractmethod
    async def manage_active_trade(self, trade_id: str, order_details: Dict[str, Any]):
        """
        Manages an active trade by placing stop-loss and take-profit orders.
        """
        pass

