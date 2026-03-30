
from pydantic import BaseModel, Field
from typing import Optional

class RiskSettings(BaseModel):
    position_size_usd: float = Field(..., gt=0, description="Fixed position size in USD")
    stop_loss_percentage: float = Field(..., gt=0, lt=100)
    max_concurrent_trades: int = Field(..., ge=1)
    max_daily_loss_usd: float = Field(..., ge=0)

class ApiKeys(BaseModel):
    binance_api_key: Optional[str] = None
    binance_api_secret: Optional[str] = None
    bybit_api_key: Optional[str] = None
    bybit_api_secret: Optional[str] = None
    kucoin_api_key: Optional[str] = None
    kucoin_api_secret: Optional[str] = None
    kucoin_api_passphrase: Optional[str] = None
    gateio_api_key: Optional[str] = None
    gateio_api_secret: Optional[str] = None
    cmc_api_key: Optional[str] = None
    telegram_bot_token: Optional[str] = None
    telegram_chat_id: Optional[str] = None

class ConfigUpdate(BaseModel):
    risk_settings: Optional[RiskSettings] = None
    api_keys: Optional[ApiKeys] = None
