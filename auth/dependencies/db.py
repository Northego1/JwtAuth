from typing import Any, AsyncGenerator
from sqlalchemy.ext.asyncio import (
    async_sessionmaker,
    create_async_engine,
    AsyncSession
)

from sqlalchemy.orm import DeclarativeBase



engine = create_async_engine(
    url='postgresql+asyncpg://postgres:0420@localhost:5432/auth'
)

async_session_session = async_sessionmaker(bind=engine, expire_on_commit=True)



async def get_db_session() -> AsyncGenerator[AsyncSession, Any]:
    async with async_session_session() as session:
        yield session


class Base(DeclarativeBase):
    pass