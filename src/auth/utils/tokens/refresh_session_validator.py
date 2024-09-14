import uuid
from datetime import datetime, timedelta, timezone

from src.auth.models import RefreshSessionModel
from src.auth.utils.constants import LABELS_FOR_LOGGER
from src.auth.utils.exceptions import (
    InvalidRefreshTokenError,
    TokenExpiredError,
)
from src.configs.logger_settings import logger


class RefreshSessionValidator:
    """
    Класс для проверки валидности сессии обновления токена.

    Methods:
        verify_refresh_session: Проверяет, соответствует ли сессия обновления
        указанному пользователю и не истек ли её срок действия.
    """

    def verify_refresh_session(
        self,
        refresh_session: RefreshSessionModel,
        user_id: uuid.UUID,
    ) -> None:
        """
        Проверяет сессию обновления токена.

        Сессия должна соответствовать указанному пользователю
        и ее срок действияне истек.

        Args:
            refresh_session (RefreshSessionModel): Объект сессии обновления.
            user_id (uuid.UUID): ID пользователя, для которого проверяется
            сессия.

        Raises:
            InvalidRefreshTokenError: Если сессия обновления токена
            не соответствует указанному пользователю.
            TokenExpiredError: Если срок действия сессии обновления истек.
        """
        if refresh_session.user_id != user_id:
            logger.info(
                (
                    'Токен обновления не соответствует пользователю.'
                    f'refresh_token_user_id = {refresh_session.user_id}'
                    f'current_user_id = {user_id}'
                ),
                labels=LABELS_FOR_LOGGER,
            )
            raise InvalidRefreshTokenError

        created_at: datetime = refresh_session.created_at
        expires_in: int = refresh_session.expires_in
        date_end: datetime = created_at + timedelta(seconds=expires_in)
        if date_end < datetime.now(timezone.utc):
            logger.info(
                (
                    'Cрок действия токена обновления истек.'
                    f'refresh_token = {refresh_session.token_id}'
                ),
                labels=LABELS_FOR_LOGGER,
            )
            raise TokenExpiredError
