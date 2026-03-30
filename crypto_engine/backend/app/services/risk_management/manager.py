
from typing import Dict, Any, Optional

from app.core.config import settings
from app.crud.trade import get_active_trades_count, get_daily_pnl

# Global kill-switch flag
KILL_SWITCH_ACTIVE = False

def calculate_dynamic_position_size(base_size: float, score: float, max_score: float = 15.0) -> float:
    """Scales position size based on signal conviction (score)."""
    # Scale between 0.5x and 1.5x of base size based on score
    multiplier = 0.5 + (score / max_score)
    multiplier = min(max(multiplier, 0.5), 1.5) # Clamp between 0.5 and 1.5
    return base_size * multiplier

async def assess_risk_and_create_order(signal: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    global KILL_SWITCH_ACTIVE

    if KILL_SWITCH_ACTIVE:
        print(f"CRITICAL: Kill-Switch is ACTIVE. Order for {signal['token_symbol']} rejected.")
        return None

    current_price = signal['market_context'].get('current_price')
    if not current_price or current_price <= 0:
        return None

    # --- Risk Checks ---
    daily_pnl = await get_daily_pnl()
    if daily_pnl <= -settings.RISK_MAX_DAILY_LOSS_USD:
        print(f"CRITICAL: Max daily loss (${settings.RISK_MAX_DAILY_LOSS_USD}) reached. ACTIVATING KILL-SWITCH.")
        KILL_SWITCH_ACTIVE = True
        return None

    active_trades = await get_active_trades_count()
    if active_trades >= settings.RISK_MAX_CONCURRENT_TRADES:
        return None

    spread_percentage = signal['market_context'].get('spread_percentage', 100)
    if spread_percentage > settings.RISK_MAX_SPREAD_PERCENTAGE:
        return None

    # --- Dynamic Sizing ---
    position_size_usd = calculate_dynamic_position_size(
        settings.RISK_FIXED_POSITION_SIZE_USD, 
        signal['score']
    )
    quantity = position_size_usd / current_price

    # --- Adaptive Stop Loss (Basic implementation based on spread) ---
    # If spread is wide, we need a wider stop loss to avoid getting chopped out instantly
    adaptive_sl_percentage = max(settings.RISK_STOP_LOSS_PERCENTAGE, spread_percentage * 2.5)
    
    stop_loss_price = current_price * (1 - (adaptive_sl_percentage / 100))
    take_profit_1_price = current_price * (1 + (settings.RISK_TP1_PERCENTAGE / 100))
    take_profit_2_price = current_price * (1 + (settings.RISK_TP2_PERCENTAGE / 100))

    # --- Smart Order Routing (Execution Hint) ---
    # Tell the execution engine to use Limit IOC if spread is manageable, otherwise Market
    order_type = "LIMIT_IOC" if spread_percentage < 1.0 else "MARKET"

    order = {
        "token_symbol": signal['token_symbol'],
        "exchange": signal['exchange'],
        "side": "BUY",
        "order_type": order_type,
        "limit_price": current_price * 1.02, # 2% slippage tolerance for Limit IOC
        "quantity": quantity,
        "position_size_usd": position_size_usd,
        "stop_loss_price": stop_loss_price,
        "take_profit_targets": [
            {"price": take_profit_1_price, "quantity_percentage": 0.5},
            {"price": take_profit_2_price, "quantity_percentage": 0.5}
        ],
        "signal_id": signal.get("id")
    }

    return order

