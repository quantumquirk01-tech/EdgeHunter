
from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.base import get_db
from app.crud.trade import get_trades_paginated
from app.api.v1.schemas.trades import TradeHistoryResponse

router = APIRouter()

@router.get("/history", response_model=TradeHistoryResponse)
async def get_trade_history(
    db: AsyncSession = Depends(get_db),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500)
):
    """
    Retrieve a paginated history of all trades.
    """
    total, trades = await get_trades_paginated(db, skip=skip, limit=limit)
    return {"total": total, "trades": trades}
