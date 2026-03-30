
from sqlalchemy import Column, Integer, String, Float, DateTime, JSON, func
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class Trade(Base):
    """
    SQLAlchemy model for storing trade data.
    This table will be the source of truth for all analytics.
    """
    __tablename__ = "trades"

    id = Column(Integer, primary_key=True, index=True)
    trade_id_exchange = Column(String, unique=True, index=True) # The ID from the exchange
    
    # Signal Details
    token_symbol = Column(String, index=True)
    exchange = Column(String, index=True)
    event_type = Column(String)
    signal_score = Column(Float)
    signal_timestamp = Column(DateTime(timezone=True), server_default=func.now())
    
    # Order Details
    order_type = Column(String, default="MARKET")
    side = Column(String, default="BUY")
    quantity = Column(Float)
    position_size_usd = Column(Float)
    
    # Execution Details
    status = Column(String, default="ACTIVE") # e.g., ACTIVE, CLOSED
    executed_price = Column(Float)
    executed_timestamp = Column(DateTime(timezone=True), server_default=func.now())
    
    # Risk Management Details
    stop_loss_price = Column(Float)
    take_profit_targets = Column(JSON)
    
    # Outcome Details
    close_price = Column(Float)
    close_timestamp = Column(DateTime(timezone=True))
    pnl_usd = Column(Float)
    closing_reason = Column(String) # e.g., 'TP1', 'SL', 'MANUAL'

