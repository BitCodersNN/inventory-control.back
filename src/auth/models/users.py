import enum
from typing import Final

import sqlalchemy as sa
from sqlalchemy import orm as so

from src.database_session import BASE

MAX_LOGIN_SIZE: Final = 32
PASS_HASH_SIZE: Final = 32
MAX_NAME_SIZE: Final = 128


class UsersRoles(enum.Enum):
    """Роли Пользователей."""

    reader = 'reader'
    writer = 'writer'
    admin = 'admin'


class UsersTable(BASE):
    """Таблица пользователей."""

    __tablename__ = 'users'

    user_id: so.Mapped[int] = so.mapped_column(
        primary_key=True,
        autoincrement=True,
    )
    login: so.Mapped[str] = so.mapped_column(
        sa.String(MAX_LOGIN_SIZE),
        unique=True,
    )
    pass_hash: so.Mapped[str] = so.mapped_column(sa.String(PASS_HASH_SIZE))
    salt: so.Mapped[str] = so.mapped_column(sa.String())
    role: so.Mapped[UsersRoles] = so.mapped_column(default=UsersRoles.reader)
    name: so.Mapped[str] = so.mapped_column(sa.String(MAX_NAME_SIZE))
