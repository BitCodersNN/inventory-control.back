import enum
import uuid
from typing import Final

import sqlalchemy as sa
from sqlalchemy import orm as so

from src.utils.database_session import BASE

MAX_LOGIN_SIZE: Final = 32
PASS_HASH_SIZE: Final = 32
MAX_NAME_SIZE: Final = 128


class UserRoles(enum.Enum):
    """
    Перечисление UserRoles определяет возможные роли пользователей в системе.

    Enum предоставляет три роли, которые могут быть назначены пользователям:
        reader: Обычный читатель, имеющий доступ только для чтения.
        writer: Пользователь с правом на запись и редактирование данных.
        admin: Администратор системы с полными правами доступа.
    """

    reader = 'reader'
    writer = 'writer'
    admin = 'admin'


class UserModel(BASE):
    """
    Класс UserModel описывает пользователя в системе.

    Атрибуты:
        user_id (UUID): Уникальный ID, автоинкрементный первичный ключ.

        login (str): Уникальный логин пользователя, ограничен по размеру.

        pass_hash (str): Хэш пароля, ограничен по размеру.

        role (UserRoles): Роль пользователя, по умолчанию 'reader'.

        name (str): Имя пользователя, ограниченное по размеру.
    """

    __tablename__ = 'users'

    user_id: so.Mapped[uuid.UUID] = so.mapped_column(
        sa.UUID(as_uuid=True),
        primary_key=True,
        index=True,
        default=uuid.uuid4,
    )
    login: so.Mapped[str] = so.mapped_column(
        sa.String(MAX_LOGIN_SIZE),
        index=True,
        unique=True,
    )
    pass_hash: so.Mapped[str] = so.mapped_column(sa.String(PASS_HASH_SIZE))
    role: so.Mapped[UserRoles] = so.mapped_column(
        sa.Enum(UserRoles, name='user_roles'),
        default=UserRoles.reader,
    )
    name: so.Mapped[str] = so.mapped_column(sa.String(MAX_NAME_SIZE))
