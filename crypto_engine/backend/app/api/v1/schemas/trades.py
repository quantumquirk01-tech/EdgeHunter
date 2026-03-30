
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class TradeBase(BaseModel):
    token_symbol: str
    exchange: str
    status: str
    pnl_usd: Optional[float] = None
    executed_price: Optional[float] = None
    close_price: Optional[float] = None

class TradeInDB(TradeBase):
    id: int
    executed_timestamp: datetime
    close_timestamp: Optional[datetime] = None

    class Config:
        from_attributes = True # Replaces orm_mode in Pydantic v2

class TradeHistoryResponse(BaseModel):
    total: int
    trades: List[TradeInDB]

