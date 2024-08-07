from typing import AsyncGenerator, Final

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import NullPool

from src.config import ASYNC_POSTGRES_URL

ENGINE: Final = create_async_engine(ASYNC_POSTGRES_URL, poolclass=NullPool)
async_session_maker = sessionmaker(
    engine=ENGINE,
    class_=AsyncSession,
    expire_on_commit=False,
)


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    """
    Asynchronously yield an SQLAlchemy AsyncSession.

    Yields:
        AsyncSession: An asynchronous SQLAlchemy session.
    """
    async with async_session_maker() as session:
        yield session
