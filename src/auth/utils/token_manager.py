from abc import ABC
from datetime import datetime, timedelta, timezone
from typing import Final
from uuid import UUID

from jose import jwt

from src.auth.models import RefreshSessionModel, UserModel
from src.auth.schemas.token import Token
from src.auth.utils.exceptions import (
    InvalidAccessTokenError,
    InvalidRefreshTokenError,
    TokenExpiredError,
)
from src.auth.utils.token_strategies.token_strategy import TokenStrategy
from src.configs.logger_settings import logger


class TokenManager:
    """
    Управление токенами доступа и обновления.

    Methods:
        create_tokens: Генерирует новые токены (доступа и обновления)
                       для указанного пользователя.

        refresh: Создаёт новые токены доступа и обновления на основе старого
                 токена обновления.

        decode_token: Декодирует токен доступа и возвращает его
                      полезную нагрузку.
    """

    _labels_for_logger: Final = {
        'service': 'auth',
        'directory': 'utils',
    }

    def __init__(self, strategy: TokenStrategy):
        """
        Инициализация класса TokenManager.

        Аргументы:
            strategy (TokenStrategy): Стратегия для создания
            и декодирования токенов.
        """
        self.strategy = strategy

    def create_tokens(
        self,
        user: UserModel,
    ) -> Token:
        """
        Создаёт новые токены доступа и обновления для пользователя.

        Args:
            user (UserModel): Модель пользователя, для которого
            создаются токены.

        Returns:
            Token: Объект Token, содержащий токены доступа и обновления.
        """
        access_token: str = self.strategy.create_access_token(user)
        refresh_token: UUID = self.strategy.create_refresh_token()
        return Token(
            access_token=access_token,
            refresh_token=refresh_token,
        )

    def refresh(
        self,
        old_refresh_token: RefreshSessionModel,
        user: UserModel,
    ) -> Token:
        """
        Создаёт токены на основе старого токена обновления.

        Проверяет валидность старого токена обновления и создаёт новые токены.

        Args:
            old_refresh_token (RefreshSessionModel): Старый токен обновления.
            user (UserModel): Модель пользователя, для которого
            обновляются токены.

        Returns:
            Token: Объект Token, содержащий новые токены доступа и обновления.

        Raises:
            InvalidRefreshTokenException: Токен обновления не соответствует
            пользователю.
            TokenExpiredException: Cрок действия токена обновления истек.
        """
        if old_refresh_token.user_id != user.user_id:
            logger.info(
                (
                    'Токен обновления не соответствует пользователю.'
                    f'refresh_token_user_id = {old_refresh_token.user_id}'
                    f'current_user_id = {user.user_id}'
                ),
                labels=cls._labels_for_logger,
            )
            raise InvalidRefreshTokenError

        created_at: datetime = old_refresh_token.created_at
        expires_in: int = old_refresh_token.expires_in
        date_end: datetime = created_at + timedelta(seconds=expires_in)
        if date_end < datetime.now(timezone.utc):
            logger.info(
                (
                    'Cрок действия токена обновления истек.'
                    f'refresh_token = {old_refresh_token.token_id}'
                ),
                labels=cls._labels_for_logger,
            )
            raise TokenExpiredError

        return self.create_tokens(user)

    def decode_token(self, access_token: str) -> dict:
        """
        Декодирует токен доступа и возвращает его полезную нагрузку.

        Args:
            access_token (str): Токен доступа для декодирования.

        Returns:
            dict: Декодированная полезная нагрузка токена.

        Raises:
            TokenExpiredException: Cрок действия токена доступа истек.
            InvalidAccessTokenException: Неверный токен доступа.
        """
        try:
            decoded_payload = self.strategy.decode_token(access_token)
        except jwt.ExpiredSignatureError:
            logger.info(
                (
                    'Cрок действия токена доступа истек.'
                    f'access_token = {access_token}'
                ),
                labels=cls._labels_for_logger,
            )
            raise TokenExpiredError
        except jwt.JWTError:
            logger.info(
                (
                    'Неверный токен доступа.'
                    f'access_token = {access_token}'
                ),
                labels=cls._labels_for_logger,
            )
            raise InvalidAccessTokenError

        return decoded_payload
