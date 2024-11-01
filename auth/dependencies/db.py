from sqlalchemy.ext.asyncio import (
    async_sessionmaker,
    create_async_engine,
    AsyncSession
)

from sqlalchemy.orm import DeclarativeBase



engine = create_async_engine(
    url='postgresql+asyncpg://postgres:0420@localhost:5432/auth'
)

Session = async_sessionmaker(bind=engine, expire_on_commit=True)



async def get_db_session():
    with Session() as session:
        yield session


class Base(DeclarativeBase):
    pass