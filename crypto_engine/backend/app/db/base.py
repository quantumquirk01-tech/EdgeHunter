
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from app.core.config import settings
from .models import Base

# Create an asynchronous engine
engine = create_async_engine(settings.DATABASE_URL, echo=True, future=True)

# Create a configured "Session" class
AsyncSessionLocal = sessionmaker(
    autocommit=False, 
    autoflush=False, 
    bind=engine, 
    class_=AsyncSession, 
    expire_on_commit=False
)

async def init_db():
    """
    Initializes the database and creates tables if they don't exist.
    This should be called on application startup.
    """
    async with engine.begin() as conn:
        # This will create all tables defined in models.py
        await conn.run_sync(Base.metadata.create_all)
        print("INFO: Database tables created (if they didn't exist).")

async def get_db() -> AsyncSession:
    """Dependency to get a DB session for API endpoints."""
    async with AsyncSessionLocal() as session:
        yield session

