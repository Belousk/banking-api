from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase

from src.config import settings


engine = create_async_engine(settings.DATABASE_URL_asyncpg, echo=True)
async_session_factory = async_sessionmaker(engine, expire_on_commit=False)

async def get_db() -> AsyncSession:
    async with async_session_factory() as session:
        yield session



class Base(DeclarativeBase):
    pass

