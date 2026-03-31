
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import asyncio
import json

from app.workers.data_worker import data_ingestion_worker
from app.workers.event_worker import event_detection_worker
from app.workers.signal_worker import signal_processing_worker
from app.core.config import settings
from app.db.base import init_db
from app.api.v1.api import api_router

# Store connected websocket clients and recent signals
class ConnectionManager:
    def __init__(self):
        self.active_connections: list[WebSocket] = []
        self.recent_signals: list[str] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)
        # Send recent signals on connect
        for signal in self.recent_signals:
            await websocket.send_text(signal)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def broadcast(self, message: str):
        # Store in recent signals (keep last 20)
        self.recent_signals.append(message)
        if len(self.recent_signals) > 20:
            self.recent_signals.pop(0)
            
        for connection in self.active_connections:
            try:
                await connection.send_text(message)
            except Exception:
                pass

manager = ConnectionManager()

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Initialize DB and start background workers
    await init_db()
    print("INFO: Starting background workers...")
    app.state.data_ingestion_task = asyncio.create_task(data_ingestion_worker())
    app.state.event_detection_task = asyncio.create_task(event_detection_worker())
    app.state.signal_processing_task = asyncio.create_task(signal_processing_worker())
    yield
    # Shutdown: Gracefully stop the background tasks
    print("INFO: Shutting down background workers...")
    app.state.data_ingestion_task.cancel()
    app.state.event_detection_task.cancel()
    app.state.signal_processing_task.cancel()
    await asyncio.gather(
        app.state.data_ingestion_task,
        app.state.event_detection_task,
        app.state.signal_processing_task,
        return_exceptions=True
    )

app = FastAPI(
    title="Crypto Opportunity Detection & Execution Engine",
    lifespan=lifespan
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS.split(",") if hasattr(settings, 'CORS_ORIGINS') else ["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.websocket("/api/v1/ws")
async def websocket_endpoint(websocket: WebSocket):
    # Allow all origins for WebSocket to prevent 403
    await manager.connect(websocket)
    try:
        while True:
            # Keep connection alive
            await websocket.receive_text()
    except WebSocketDisconnect:
        manager.disconnect(websocket)

@app.get("/health", tags=["Health Check"])
def health_check():
    """Simple health check endpoint to confirm the API is running."""
    return {"status": "ok"}

@app.get("/api/v1/trades/recent")
async def get_recent_signals():
    """Returns the cached recent signals."""
    return [json.loads(s) for s in manager.recent_signals]

@app.post("/api/v1/mock-event")
async def trigger_mock_event():
    """Triggers a mock Launchpool event for testing the UI."""
    from app.workers.event_worker import Redis
    redis_client = Redis.from_url(settings.REDIS_URL, decode_responses=True)
    mock_event = {
        "source": "binance",
        "title": "Binance Will List EdgeHunter Token (EHT) on Launchpool",
        "url": "https://www.binance.com/en/support/announcement/mock-eht",
        "timestamp": int(asyncio.get_event_loop().time())
    }
    await redis_client.lpush(settings.REDIS_RAW_EVENTS_QUEUE, json.dumps(mock_event))
    return {"status": "Mock event queued", "event": mock_event}

app.include_router(api_router, prefix=settings.API_V1_STR)

