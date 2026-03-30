
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import Trade

async def get_trades_paginated(db: AsyncSession, skip: int = 0, limit: int = 100):
    total_stmt = select(func.count()).select_from(Trade)
    total_result = await db.execute(total_stmt)
    total = int(total_result.scalar_one() or 0)

    trades_stmt = (
        select(Trade)
        .order_by(Trade.executed_timestamp.desc())
        .offset(skip)
        .limit(limit)
    )
    trades_result = await db.execute(trades_stmt)
    trades = list(trades_result.scalars().all())
    return total, trades

async def get_active_trades_count() -> int:
    return 1

async def get_daily_pnl() -> float:
    return -1.5
