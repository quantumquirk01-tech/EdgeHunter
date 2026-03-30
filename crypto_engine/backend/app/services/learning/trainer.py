
from typing import Dict, Any

# This is a conceptual representation of the learning engine.
# A real system would use a more sophisticated model to update weights,
# possibly involving statistical analysis or machine learning on a large dataset of trades.

def analyze_trade_outcome(trade_result: Dict[str, Any], signal: Dict[str, Any]):
    """
    Analyzes the outcome of a completed trade and logs insights
    that can be used to manually or automatically tune the Signal Engine weights.

    Args:
        trade_result: A dictionary containing the final state of the trade (e.g., PnL, closing reason).
        signal: The original signal that triggered this trade.
    """
    pnl = trade_result.get("pnl_usd", 0)
    closing_reason = trade_result.get("closing_reason") # e.g., 'TP1', 'SL'
    initial_score = signal.get("score")

    print("\n--- LEARNING ENGINE: POST-TRADE ANALYSIS ---")
    print(f"Trade for {signal['token_symbol']} on {signal['exchange']} completed.")
    print(f"Initial Signal Score: {initial_score}, Final PnL: ${pnl:.2f}, Reason: {closing_reason}")

    # --- Generate Learning Insights ---

    if pnl > 0:
        # Positive outcome: The signal was good.
        print("Insight: Successful trade. The scoring factors in the original signal were likely correct.")
        print(f"  - Factors: Exchange ({signal['exchange']}), Score ({initial_score}), Liquidity (${signal['market_context']['liquidity_usd']})")
        print("  - Recommendation: Consider slightly increasing weights for factors present in this signal if this pattern repeats.")

    elif pnl < 0:
        # Negative outcome: The signal was a false positive.
        print("Insight: Failed trade (Stop-Loss hit). The signal was a false positive.")
        print(f"  - Factors: Exchange ({signal['exchange']}), Score ({initial_score})")
        print("  - Recommendation: Analyze what went wrong. Was the initial liquidity fake? Was it a pump and dump?")
        
        # Example of a specific rule-based insight
        if signal['market_context']['liquidity_usd'] > 100000:
             print("  - Specific Insight: High initial liquidity might be a 'crowded trade' indicator. Consider adding or increasing a penalty for high liquidity.")
        
        if initial_score > 10: # A very high score that still failed
             print("  - Specific Insight: A very high-scoring signal failed. This is a high-priority event to analyze. A core assumption might be wrong.")

    print("--- END ANALYSIS ---\n")

    # In a fully automated system, this function could write these insights to a database
    # or even directly trigger a gradual weight adjustment process.
    # For now, it provides logs for manual review.

