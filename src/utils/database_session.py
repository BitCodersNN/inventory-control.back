import contextlib
from typing import AsyncGenerator, Callable, Final

from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.pool import NullPool

from src.configs.db_config import ASYNC_POSTGRES_URL
from src.configs.logger_settings.logger_config import logger

BASE: Final = declarative_base()

ENGINE: Final = create_async_engine(ASYNC_POSTGRES_URL, poolclass=NullPool)

ASYNC_SESSION_MAKER: Final = async_sessionmaker(
    ENGINE,
    class_=AsyncSession,
    expire_on_commit=False,
)


async def session_connect(func: Callable, *args, **kwargs):
    """
     Выполняет функцию в а синхронной сессией базы данных.

    Args:
        func (Callable): Функция, выполняемая в контексте сессии.
        args: Аргументы для переданной функции.
        kwargs: Ключевые аргументы для переданной функции.

    Returns:
        Any: Результат выполнения переданной функции.
    """
    async with get_async_session() as session:
        func_result = await func(session, *args, **kwargs)
        await session.commit()
    return func_result


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
    except Exception as ex:
        logger.exception(
            'Произошла ошибка при работе с БД\nError: {0}'.format(
                str(ex),
            ),
        )
        raise
