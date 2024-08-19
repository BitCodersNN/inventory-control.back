from typing import Final

from sqlalchemy import event
from sqlalchemy.orm import Session

from src.auth.models.refresh_tokens import RefreshTokenModel

MAX_TOKEN_COUNT: Final = 5


@event.listens_for(RefreshTokenModel, 'before_insert')
def limit_refresh_tokens(mapper, connection, target):
    """
    Ограничивает количество refresh токенов для пользователя до MAX_TOKEN_COUNT.

    Args:
        mapper: Объект маппера.
        connection: Объект соединения с базой данных.
        target: Объект модели, который будет вставлен.

    Raises:
        ValueError: Если у пользователя уже есть MAX_TOKEN_COUNT
        или более токенов.
    """
    session = Session(bind=connection)
    token_count = session.query(RefreshTokenModel).filter(
        RefreshTokenModel.user_id == target.user_id,
    ).count()
    if token_count >= MAX_TOKEN_COUNT:
        raise ValueError(
            'User cannot have more than MAX_TOKEN_COUNT refresh tokens',
        )
