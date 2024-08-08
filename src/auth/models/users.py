import sqlalchemy as sa
import sqlalchemy.orm as so
import enum

from src.database_session import BASE


class UsersRoles(enum.Enum):
    """Роли Пользователей"""

    reader = 'reader'
    writer = 'writer'
    admin = 'admin'


class UsersTable(BASE):
    """Таблица пользователей"""

    __tablename__ = 'users'

    user_id: so.Mapped[int] = so.mapped_column(primary_key=True, autoincrement=True)
    login: so.Mapped[str] = so.mapped_column(sa.String(20), unique=True)
    pass_hash: so.Mapped[str] = so.mapped_column(sa.String(32))
    salt: so.Mapped[str] = so.mapped_column(sa.String(20))
    role: so.Mapped[UsersRoles] = so.mapped_column(default=UsersRoles.reader)
    name: so.Mapped[str] = so.mapped_column(sa.String(32))


