import contextlib
from typing import AsyncGenerator, Final

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import NullPool

from src.configs.logger.logger_config import logger
from src.configs.db_config import ASYNC_POSTGRES_URL

BASE: Final = declarative_base()

ENGINE: Final = create_async_engine(ASYNC_POSTGRES_URL, poolclass=NullPool)

ASYNC_SESSION_MAKER: Final = sessionmaker(
    engine=ENGINE,
    class_=AsyncSession,
    expire_on_commit=False,
)


@contextlib.asynccontextmanager
async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    """
    Asynchronously yield an SQLAlchemy AsyncSession.

    Yields:
        AsyncSession: An asynchronous SQLAlchemy session.
    """
    try:
        async with ASYNC_SESSION_MAKER() as session:
            yield session
    except SQLAlchemyError as ex:
        logger.exception(
            'Не удалось создать сессию с БД! \nSQLAlchemy error: {0}'.format(str(ex)),
        )
        if session is not None:
            await session.rollback()
        raise ex
    finally:
        if session is not None:
            await session.close()
