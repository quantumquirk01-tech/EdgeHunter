
from fastapi import APIRouter

from app.core.config import settings
from app.api.v1.schemas.config import ConfigUpdate

router = APIRouter()

@router.get("/settings")
def get_current_settings():
    """
    Retrieve the current risk management settings.
    API keys are not exposed for security.
    """
    return {
        "risk_settings": {
            "position_size_usd": settings.RISK_FIXED_POSITION_SIZE_USD,
            "stop_loss_percentage": settings.RISK_STOP_LOSS_PERCENTAGE,
            "max_concurrent_trades": settings.RISK_MAX_CONCURRENT_TRADES,
            "max_daily_loss_usd": settings.RISK_MAX_DAILY_LOSS_USD
        }
    }

@router.post("/settings")
def update_settings(update: ConfigUpdate):
    if update.risk_settings:
        risk = update.risk_settings.model_dump(exclude_none=True)
        settings.RISK_FIXED_POSITION_SIZE_USD = risk.get("position_size_usd", settings.RISK_FIXED_POSITION_SIZE_USD)
        settings.RISK_STOP_LOSS_PERCENTAGE = risk.get("stop_loss_percentage", settings.RISK_STOP_LOSS_PERCENTAGE)
        settings.RISK_MAX_CONCURRENT_TRADES = risk.get("max_concurrent_trades", settings.RISK_MAX_CONCURRENT_TRADES)
        settings.RISK_MAX_DAILY_LOSS_USD = risk.get("max_daily_loss_usd", settings.RISK_MAX_DAILY_LOSS_USD)
        print(f"INFO: Risk settings updated: {risk}")
    if update.api_keys:
        api_keys = update.api_keys.model_dump(exclude_none=True)
        mapping = {
            "binance_api_key": "BINANCE_API_KEY",
            "binance_api_secret": "BINANCE_API_SECRET",
            "bybit_api_key": "BYBIT_API_KEY",
            "bybit_api_secret": "BYBIT_API_SECRET",
            "kucoin_api_key": "KUCOIN_API_KEY",
            "kucoin_api_secret": "KUCOIN_API_SECRET",
            "kucoin_api_passphrase": "KUCOIN_API_PASSPHRASE",
            "gateio_api_key": "GATEIO_API_KEY",
            "gateio_api_secret": "GATEIO_API_SECRET",
            "cmc_api_key": "CMC_API_KEY",
            "telegram_bot_token": "TELEGRAM_BOT_TOKEN",
            "telegram_chat_id": "TELEGRAM_CHAT_ID"
        }
        updated_count = 0
        for payload_key, settings_key in mapping.items():
            value = api_keys.get(payload_key)
            if value is not None:
                setattr(settings, settings_key, value)
                updated_count += 1
        print(f"INFO: {updated_count} API key(s) updated")
    return {"status": "success", "message": "Settings updated successfully."}
