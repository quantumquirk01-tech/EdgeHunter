
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

async def get_active_trades_count(db: AsyncSession) -> int:
    stmt = select(func.count()).select_from(Trade).where(Trade.status == "ACTIVE")
    result = await db.execute(stmt)
    return int(result.scalar_one() or 0)

async def get_daily_pnl(db: AsyncSession) -> float:
    from datetime import datetime, timezone
    today_start = datetime.now(timezone.utc).replace(hour=0, minute=0, second=0, microsecond=0)
    stmt = select(func.coalesce(func.sum(Trade.pnl_usd), 0.0)).where(
        Trade.status == "CLOSED",
        Trade.close_timestamp >= today_start
    )
    result = await db.execute(stmt)
    return float(result.scalar_one() or 0.0)
