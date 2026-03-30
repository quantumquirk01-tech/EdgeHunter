
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # API Keys
    CMC_API_KEY: str = "YOUR_COINMARKETCAP_API_KEY"
    BINANCE_API_KEY: str = "YOUR_BINANCE_API_KEY"
    BINANCE_API_SECRET: str = "YOUR_BINANCE_API_SECRET"
    BYBIT_API_KEY: str = "YOUR_BYBIT_API_KEY"
    BYBIT_API_SECRET: str = "YOUR_BYBIT_API_SECRET"
    KUCOIN_API_KEY: str = "YOUR_KUCOIN_API_KEY"
    KUCOIN_API_SECRET: str = "YOUR_KUCOIN_API_SECRET"
    KUCOIN_API_PASSPHRASE: str = "YOUR_KUCOIN_API_PASSPHRASE"
    GATEIO_API_KEY: str = "YOUR_GATEIO_API_KEY"
    GATEIO_API_SECRET: str = "YOUR_GATEIO_API_SECRET"
    TELEGRAM_BOT_TOKEN: str = "YOUR_TELEGRAM_BOT_TOKEN"
    TELEGRAM_CHAT_ID: str = "YOUR_TELEGRAM_CHAT_ID"

    # Database & Cache
    DATABASE_URL: str = "postgresql+asyncpg://user:password@localhost/crypto_engine"
    REDIS_URL: str = "redis://localhost:6379"

    # Redis Queues
    REDIS_RAW_EVENTS_QUEUE: str = "raw_events"
    REDIS_PARSED_EVENTS_QUEUE: str = "parsed_events"

    # Worker Settings
    DATA_INGESTION_POLL_INTERVAL: int = 8 # seconds

    # Signal Engine Settings
    SIGNAL_MAX_EVENT_AGE_SECONDS: int = 30 # Ignore events older than this

    # Risk Management Settings (Based on user input)
    RISK_LEVEL: str = "AGGRESSIVE_FORCED_BY_CAPITAL" # Was 'Moderate'
    RISK_FIXED_POSITION_SIZE_USD: float = 10.0 # Fixed amount due to low capital
    RISK_STOP_LOSS_PERCENTAGE: float = 8.0 # 5-8% for Moderate
    RISK_TP1_PERCENTAGE: float = 20.0
    RISK_TP2_PERCENTAGE: float = 50.0
    RISK_MAX_CONCURRENT_TRADES: int = 3
    RISK_MAX_DAILY_LOSS_USD: float = 10.0 # 5% of $200 capital
    RISK_MAX_SPREAD_PERCENTAGE: float = 2.0 # Don't enter if spread is > 2%

    # API V1 STR
    API_V1_STR: str = "/api/v1"
    SECRET_KEY: str = "a_very_secret_key_for_jwt_and_encryption"
    ALGORITHM: str = "HS256"

    class Config:
        env_file = ".env"
        env_file_encoding = 'utf-8'

settings = Settings()

