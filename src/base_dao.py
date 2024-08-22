from typing import Generic, Optional, Sequence, TypeVar

from pydantic import BaseModel
from sqlalchemy import CursorResult, Result, func, select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import Select

from src.configs.logger.logger_config import logger
from src.database_session import BASE

ModelType = TypeVar('ModelType', bound=BASE)
CreateSchemeType = TypeVar('CreateSchemeType', bound=BaseModel)
UpdateSchemeType = TypeVar('UpdateSchemeType', bound=BaseModel)

_LOGGER_MESSAGE = (
    'Ошибка выполнения запроса в {class}.{method} ' +
    'с фильтрами: {filters}, filters_by: {filters_by}. ' +
    'Ошибка: {ex}'
)


class BaseDAO(Generic[ModelType, CreateSchemeType, UpdateSchemeType]):
    """
    Базовый класс для работы с данными (DAO).

    Предоставляет общие методы для выполнения запросов к базе данных.

    Атрибуты:
        model: Класс модели данных SQLAlchemy.

    Методы:
        find_one_or_none: Асинхронно находит одну запись
        или None, если записи нет по заданным фильтрам или возникла ошибка.
        find_all: Асинхронно находит все записи по заданным фильтрам
        или None, если возникла ошибка.
    """

    model = None

    @classmethod
    async def find_one_or_none(
        cls,
        session: AsyncSession,
        *filters,
        **filters_by,
    ) -> Optional[ModelType]:
        """
        Находит одну запись или None по заданным фильтрам.

        Аргументы:
            session: Асинхронная сессия SQLAlchemy.
            filters: Фильтры для метода filter.
            filters_by: Фильтры для метода filter_by.

        Возвращает:
            Optional[ModelType]: Найденную запись или None,
            если запись не найдена.
        """
        query: Select = select(
            cls.model,
        ).filter(
            *filters,
        ).filter_by(
            **filters_by,
        )

        try:
            query_result = await cls._execute_query(session, query)
        except Exception as ex:
            return cls._log_error('find_one_or_none', filters, filters_by, ex)
        return query_result.scalars().one_or_none()

    @classmethod
    async def find_all(  # noqa: WPS211
        cls,
        session: AsyncSession,
        offset: int = 0,
        limit: int = 100,
        *filters,
        **filters_by,
    ) -> Optional[Sequence[ModelType]]:
        """
        Находит все записи по заданным фильтрам.

        Аргументы:
            session: Асинхронная сессия SQLAlchemy.
            offset: Смещение для запроса.
            limit: Лимит на количество возвращаемых записей.
            filters: Фильтры для метода filter.
            filters_by: Фильтры для метода filter_by.

        Возвращает:
            Optional[Sequence[ModelType]]: Список найденных записей или None,
            если произошла ошибка.
        """
        query: Select = select(
            cls.model,
        ).filter(
            *filters,
        ).filter_by(
            **filters_by,
        ).offset(
            offset,
        ).limit(
            limit,
        )

        try:
            query_result = await cls._execute_query(session, query)
        except Exception as ex:
            return cls._log_error('find_all', filters, filters_by, ex)
        return query_result.scalars().all()

    @classmethod
    async def count(
        cls,
        session: AsyncSession,
        *filters,
        **filters_by,
    ) -> Optional[int]:
        """
        Подсчитывает количество записей, соответствующих заданным фильтрам.

        Аргументы:
            session (AsyncSession): Асинхронная сессия базы данных.
            filters: Позиционные фильтры.
            filters_by: Фильтры по ключевым словам.

        Возвращает:
            Optional[int]: Количество записей или None в случае ошибки.
        """
        query: Select = select(
            func.count(),
        ).select_from(
            cls.model,
        ).filter(
            *filters,
        ).filter_by(
            **filters_by,
        )
        try:
            query_result = await cls._execute_query(session, query)
        except Exception as ex:
            return cls._log_error('count', filters, filters_by, ex)
        return query_result.scalar()

    @classmethod
    async def _execute_query(
        cls,
        session: AsyncSession,
        query: Select,
    ) -> Optional[Result | CursorResult]:
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

    @classmethod
    def _log_error(
        cls,
        method_name: str,
        filters,
        filters_by,
        ex: Exception,
    ) -> None:
        """
        Логирует ошибку, связанную с выполнением метода класса.

        Аргументы:
            method_name: Имя метода, в котором произошла ошибка.
            filters: Фильтры, использованные в запросе.
            filters_by: Фильтры полей, использованные в запросе.
            ex: Исключение, которое было вызвано.
        """
        labels = {'Error name': type(ex).__name__}
        if isinstance(ex, SQLAlchemyError):
            labels['Table name'] = cls.model.__tablename__

        logger.error(
            _LOGGER_MESSAGE.format(
                class_name=cls.__name__,
                method_name=method_name,
                filters=filters,
                filters_by=filters_by,
                ex=ex,
            ),
            exc_info=True,
            labels=labels,
        )
