from typing import Optional, Union

from sqlalchemy import CursorResult, Result
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import Delete, Insert, Select, Update


async def execute_query(
    session: AsyncSession,
    query: Union[Select, Insert, Delete, Update],
) -> Optional[Union[Result, CursorResult]]:
    """
    Выполняет запрос к базе данных.

    Аргументы:
        session: Асинхронная сессия SQLAlchemy.
        query: SQLAlchemy запрос.

    Возвращает:
        Optional[Result | CursorResult]: Результат выполнения запроса.
    """
    async with session.begin():
        query_result = await session.execute(query)
    return query_result
