import enum
from typing import Final

import sqlalchemy as sa
from sqlalchemy import orm as so

from src.database_session import BASE

login_size: Final = 20
pass_hash_size: Final = 32
name_size: Final = 32


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
        sa.String(login_size),
        unique=True,
    )
    pass_hash: so.Mapped[str] = so.mapped_column(sa.String(pass_hash_size))
    salt: so.Mapped[str] = so.mapped_column(sa.String())
    role: so.Mapped[UsersRoles] = so.mapped_column(default=UsersRoles.reader)
    name: so.Mapped[str] = so.mapped_column(sa.String(name_size))
