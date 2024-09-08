from typing import Any, Dict, List, Optional, Union

from sqlalchemy import CursorResult, Result
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import Delete, Insert, Select, Update


async def execute_query(
    session: AsyncSession,
    query: Union[Select, Insert, Delete, Update],
    data_in: List[Dict[str, Any]] = None,
) -> Optional[Union[Result, CursorResult]]:
    """
    Выполняет запрос к базе данных.

    Args:
        session: Асинхронная сессия SQLAlchemy.
        query: SQLAlchemy запрос.
        data_in: Дополнительные данные для запроса (по умолчанию None).

    Returns:
        Optional[Result | CursorResult]: Результат выполнения запроса.
    """
    async with session.begin():
        query_result = await session.execute(query, data_in)
    return query_result
