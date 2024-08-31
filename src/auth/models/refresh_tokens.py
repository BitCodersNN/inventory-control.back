import uuid
from datetime import datetime

import sqlalchemy as sa
from sqlalchemy import event, func
from sqlalchemy import orm as so
from sqlalchemy import select
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql.expression import false

from src.auth.utils.constants import MAX_TOKEN_COUNT
from src.utils.database_session import BASE


class RefreshTokenModel(BASE):
    """
    Модель для хранения информации о refresh токенах.

    Атрибуты:
        token_id (int): Уникальный идентификатор токена, автоинкрементный,
                        первичный ключ.

        refresh_token (uuid.UUID): Уникальный идентификатор refresh токена.

        expires_in (int): Время жизни токена в секундах.

        created_at (datetime): Время создания токена, устанавливается
                               автоматически при создании записи.

        revoked (bool): Флаг, указывающий, был ли токен отозван.
                        По умолчанию False.

        user_id (uuid.UUID): Идентификатор пользователя, к которому относится
                             токен, связь по внешнему ключу с таблицей 'users'.

    """

    __tablename__ = 'refresh_tokens'

    token_id: so.Mapped[int] = so.mapped_column(
        primary_key=True,
        index=True,
        autoincrement=True,
    )
    refresh_token: so.Mapped[uuid.UUID] = so.mapped_column(
        UUID,
        index=True,
    )
    expires_in: so.Mapped[int]
    created_at: so.Mapped[datetime] = so.mapped_column(
        sa.TIMESTAMP(timezone=True),
        server_default=func.now(),
    )
    revoked: so.Mapped[bool] = so.mapped_column(default=False)
    user_id: so.Mapped[uuid.UUID] = so.mapped_column(
        UUID,
        sa.ForeignKey('users.user_id', ondelete='CASCADE'),
    )


@event.listens_for(RefreshTokenModel, 'before_insert')
def check_token_limit(mapper, connection, target):
    """
    Проверка лимита токенов перед вставкой.

    Args:
        mapper: Маппер модели.
        connection: Соединение с БД.
        target: Экземпляр модели.

    Raises:
        ValueError: Если превышен лимит токенов.
    """
    query = select(
        func.count(),
    ).filter(
        RefreshTokenModel.user_id == target.user_id,
        RefreshTokenModel.revoked == false(),
    )
    result_of_query = connection.execute(query)
    count = result_of_query.scalar()
    if count >= MAX_TOKEN_COUNT:
        raise ValueError(
            f'Превышен лимит токенов у пользователя c id: {target.user_id}.',
        )
