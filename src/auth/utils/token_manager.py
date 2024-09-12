from datetime import datetime, timedelta, timezone
from typing import Final
from uuid import UUID, uuid4

from jose import jwt

from src.auth.models import RefreshSessionModel, UserModel
from src.auth.schemas.token import Token
from src.auth.utils.exceptions import (
    InvalidAccessTokenError,
    InvalidRefreshTokenError,
    TokenExpiredError,
)
from src.configs.logger_settings import logger
from src.configs.token_config import (
    ACCESS_TOKEN_EXPIRE_SECONDS,
    SECRET_KEY,
    TOKEN_ALG,
)


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

    @classmethod
    async def create_tokens(
        cls,
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
        access_token: str = await cls._create_access_token(user)
        refresh_token: UUID = await cls._create_refresh_token()
        return Token(
            access_token=access_token,
            refresh_token=refresh_token,
        )

    @classmethod
    async def refresh(
        cls,
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

        return await cls.create_tokens(user)

    @classmethod
    async def decode_token(cls, access_token: str) -> dict:
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
            decoded_payload = jwt.decode(
                access_token,
                SECRET_KEY,
                algorithms=[TOKEN_ALG],
            )
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

    @classmethod
    async def _create_access_token(
        cls,
        user: UserModel,
    ) -> str:
        """
        Создаёт новый токен доступа для пользователя.

        Args:
            user (UserModel): Модель пользователя, для которого создаётся токен.

        Returns:
            str: Сгенерированный токен доступа.
        """
        created_at: datetime = datetime.now(timezone.utc)
        exp = timedelta(seconds=ACCESS_TOKEN_EXPIRE_SECONDS)
        exp += created_at
        token_data: dict = {
            'sub': user.user_id,
            'iat': created_at,
            'exp': exp,
        }
        return jwt.encode(
            token_data,
            key=SECRET_KEY,
            algorithm=TOKEN_ALG,
        )

    @classmethod
    async def _create_refresh_token(
        cls,
    ) -> UUID:
        """
        Создаёт новый токен обновления для пользователя.

        Returns:
            UUID: Сгенерированный токен обновления.
        """
        return uuid4()
