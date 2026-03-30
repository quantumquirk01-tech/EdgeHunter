
from fastapi import APIRouter

from .endpoints import trades, config

api_router = APIRouter()
api_router.include_router(trades.router, prefix="/trades", tags=["Trades"])
api_router.include_router(config.router, prefix="/config", tags=["Configuration"])

