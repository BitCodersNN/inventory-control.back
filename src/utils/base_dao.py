from typing import Any, Dict, Generic, List, Optional, Sequence, TypeVar, Union

from pydantic import BaseModel
from sqlalchemy import delete, func, insert, select, update
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import Delete, Insert, Select, Update

from src.configs.logger.logger_config import logger
from src.utils.database_session import BASE
from src.utils.db_query_executor import execute_query

ModelType = TypeVar('ModelType', bound=BASE)
CreateSchemeType = TypeVar('CreateSchemeType', bound=BaseModel)
UpdateSchemeType = TypeVar('UpdateSchemeType', bound=BaseModel)


class BaseDAO(   # noqa: WPS214
    Generic[ModelType, CreateSchemeType, UpdateSchemeType],
):
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
        count: Асинхронно подсчитывает количество записей по заданным фильтрам
        или None, если возникла ошибка.
        add: Асинхронно добавляет новую запись в базу данных.
        delete: Асинхронно удаляет записи из базы данных по заданным фильтрам.
        update: Асинхронно обновляет запись в базе данных.
        add_bulk: Асинхронно массово добавляет записи в базу данных.
        update_bulk: Асинхронно массово обновляет записи в базе данных.

    Этот класс служит основой для создания DAO-классов, которые могут быть
    специализированы для работы с конкретными моделями данных.
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
        query: Select = (
            select(cls.model).
            filter(*filters).
            filter_by(**filters_by)
        )

        try:
            query_result = await execute_query(session, query)
        except Exception as ex:
            return cls._log_error(
                'find_one_or_none',
                ex,
                filters=filters,
                filters_by=filters_by,
            )
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
        query: Select = (
            select(cls.model).
            filter(*filters).
            filter_by(**filters_by).
            offset(offset).
            limit(limit)
        )

        try:
            query_result = await execute_query(session, query)
        except Exception as ex:
            return cls._log_error(
                'find_all',
                ex,
                filters=filters,
                filters_by=filters_by,
            )
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
            filters: Фильтры для метода filter.
            filters_by: Фильтры для метода filter_by.

        Возвращает:
            Optional[int]: Количество записей или None в случае ошибки.
        """
        query: Select = (
            select(func.count()).
            select_from(cls.model).
            filter(*filters).
            filter_by(**filters_by)
        )
        try:
            query_result = await execute_query(session, query)
        except Exception as ex:
            return cls._log_error(
                'count',
                ex,
                filters=filters,
                filters_by=filters_by,
            )
        return query_result.scalar()

    @classmethod
    async def add(
        cls,
        session: AsyncSession,
        obj_in: Union[CreateSchemeType, Dict[str, Any]],
    ) -> Optional[ModelType]:
        """
        Добавляет новую запись в базу данных.

        Аргументы:
            session (AsyncSession): Асинхронная сессия базы данных.
            obj_in (Union[CreateSchemeType, Dict[str, Any]]): Данные для
            создания новой записи, которые могут быть либо экземпляром
            CreateSchemeType, либо словарем.

        Возвращает:
            Optional[ModelType]: Созданная запись в базе данных
            или None в случае ошибки.
        """
        create_data = (
            obj_in if isinstance(obj_in, dict)
            else obj_in.model_dump(exclude_unset=True)
        )
        query: Insert = (
            insert(cls.model).
            values(**create_data).
            returning(cls.model)
        )
        try:
            query_result = await execute_query(session, query)
        except Exception as ex:
            return cls._log_error('add', ex, data=create_data)
        return query_result.scalars().first()

    @classmethod
    async def delete(
        cls,
        session: AsyncSession,
        *filters,
        **filters_by,
    ) -> Optional[int]:
        """
        Удаляет записи из базы данных, соответствующие заданным фильтрам.

        Аргументы:
            session (AsyncSession): Асинхронная сессия базы данных.
            filters: Фильтры для метода filter.
            filters_by: Фильтры для метода filter_by.

        Возвращает:
            Optional[int]: Количество удаленных строк или None в случае ошибки.
        """
        query: Delete = (
            delete(cls.model).
            filter(*filters).
            filter_by(**filters_by)
        )
        try:
            query_result = await execute_query(session, query)
        except Exception as ex:
            return cls._log_error(
                'delete',
                ex,
                filters=filters,
                filters_by=filters_by,
            )
        return query_result.rowcount()

    @classmethod
    async def update(
        cls,
        session: AsyncSession,
        *where,
        obj_in: Union[UpdateSchemeType, Dict[str, Any]],
    ) -> Optional[ModelType]:
        """
        Обновляет запись в базе данных на основе переданных параметров.

        Аргументы:
            session (AsyncSession): Асинхронная сессия базы данных.
            where: Условия для выборки записи, которую нужно обновить.
            obj_in (Union[UpdateSchemeType, Dict[str, Any]]): Данные
            для обновления, могут быть представлены как экземпляром
            схемы обновления, так и словарем.

        Возвращает:
            Обновленный экземпляр модели или None в случае ошибки.
        """
        update_data = (
            obj_in if isinstance(obj_in, dict)
            else obj_in.model_dump(exclude_unset=True)
        )
        query: Update = (
            update(cls.model).
            where(*where).
            values(**update_data).
            returning(cls.model)
        )
        try:
            query_result = await execute_query(session, query)
        except Exception as ex:
            return cls._log_error(
                'update',
                ex,
                where=where,
                data=update_data,
            )
        return query_result.scalars().one()

    @classmethod
    async def add_bulk(
        cls,
        session: AsyncSession,
        data_in: List[Dict[str, Any]],
    ) -> Optional[Sequence[ModelType]]:
        """
        Массово добавляет записи в базу данных.

        Аргументы:
            session (AsyncSession): Асинхронная сессия базы данных.
            data (List[Dict[str, Any]]): Список словарей, содержащих
            данные для вставки.

        Возвращает:
            Последовательность объектов модели или None в случае ошибки.
        """
        query: Insert = insert(cls.model).returning(cls.model)
        try:
            query_result = await execute_query(session, query, data_in)
        except Exception as ex:
            return cls._log_error(
                'add_bulk',
                ex,
                data=data_in,
            )
        return query_result.scalars().all()

    @classmethod
    async def update_bulk(
        cls,
        session: AsyncSession,
        data_in: List[Dict[str, Any]],
    ) -> Optional[Sequence[ModelType]]:
        """
        Массово обновляет записи в базе данных.

        Аргументы:
            session (AsyncSession): Асинхронная сессия базы данных.
            data_in (List[Dict[str, Any]]): Список словарей, содержащих
            данные для вставки.

        Возвращает:
            Последовательность объектов модели или None в случае ошибки.
        """
        query: Update = update(cls.model).returning(cls.model)
        try:
            query_result = await execute_query(session, query, data_in)
        except Exception as ex:
            return cls._log_error(
                'update_bulk',
                ex,
                data=data_in,
            )
        return query_result.scalars().all()

    @classmethod
    def _log_error(
        cls,
        method_name: str,
        ex: Exception,
        **kwargs,
    ) -> None:
        """
        Логирует ошибку, связанную с выполнением метода класса.

        Аргументы:
            method_name: Имя метода, в котором произошла ошибка.
            ex: Исключение, которое было вызвано.
            kwargs: Дополнительные параметры для логирования.
        """
        labels = {'Error name': type(ex).__name__}
        if isinstance(ex, SQLAlchemyError):
            labels['Table name'] = cls.model.__tablename__

        message_parts = [
            f'Ошибка выполнения запроса в {cls.__name__}.{method_name}',
        ]

        for key, argument in kwargs.items():
            if argument is not None:
                message_parts.append(f'{key.capitalize()}: {argument}')

        message_parts.append(f'Ошибка: {ex}')

        log_message = ' '.join(message_parts)

        logger.error(
            log_message,
            exc_info=True,
            labels=labels,
        )
