from datetime import datetime, timedelta, timezone
from typing import Optional
from uuid import UUID, uuid4

import jwt
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.dao.refresh_token import RefreshTokenDAO
from src.auth.models import RefreshTokenModel, UserModel
from src.auth.schemas.refresh_token import RefreshTokenCreate
from src.auth.schemas.token import Token
from src.configs.token_config import (
    ACCESS_TOKEN_EXPIRE_SECONDS,
    REFRESH_TOKEN_EXPIRE_SECONDS,
    SECRET_KEY,
    TOKEN_ALG,
)


class TokenManager:
    """
    Класс для управления токенами: создание, обновление и валидация.

    Methods:
        create_tokens: Генерирует новые токены (доступа и обновления)
                       для указанного пользователя.

        refresh: Обновляет токен доступа, используя токен обновления.

        decode_token: Проверяет действительность токена доступа.
    """

    @classmethod
    async def create_tokens(
        cls,
        session: AsyncSession,
        user: UserModel,
    ) -> Token:
        """
        Создаёт токены доступа и обновления для пользователя.

        Args:
            session (AsyncSession): Сессия базы данных.
            user (UserModel): Пользователь.

        Returns:
            Token: Объект с током доступа и обновления.

        Raises:
            ValueError: Если пользователь не найден.
        """
        access_token: str = await cls._create_access_token(session, user)
        refresh_token: UUID = await cls._create_refresh_token(session, user)
        return Token(access_token=access_token, refresh_token=refresh_token)

    @classmethod
    async def refresh(
        cls,
        session: AsyncSession,
        old_refresh_token: RefreshTokenModel,
        user: UserModel,
    ) -> Token:
        """
        Обновляет токены доступа и обновления.

        Args:
            session (AsyncSession): Сессия базы данных.
            old_refresh_token (RefreshTokenModel): Токен обновления.
            user (UserModel): Пользователь.

        Returns:
            Token: Новый токен доступа и обновления.

        Raises:
            ValueError: Если токен не найден или не устарел.
        """
        if old_refresh_token.user_id != user.user_id:
            raise ValueError('user_id != user_id')

        created_at: datetime = old_refresh_token.created_at
        expires_in: int = int(old_refresh_token.expires_in)
        date_end: datetime = created_at + timedelta(seconds=expires_in)
        if date_end < datetime.now(timezone.utc):
            raise ValueError('Рефреш токен устарел.')

        RefreshTokenDAO.update(
            session,
            RefreshTokenModel.token_id == old_refresh_token.token_id,
            obj_in={'revoked': True},
        )

        return Token(
            access_token=await cls._create_access_token(session, user),
            refresh_token=await cls._create_refresh_token(session, user),
        )

    @classmethod
    async def decode_token(cls, access_token: str) -> Optional[dict]:
        """
        Проверяет корректность токена доступа.

        Args:
            access_token (str): Токен доступа.

        Returns:
            dict: {data}, если токен валиден, иначе {}.
        """
        try:
            decoded_payload = jwt.decode(
                access_token,
                SECRET_KEY,
                algorithms=[TOKEN_ALG],
            )
        except jwt.ExpiredSignatureError:
            return None
        except jwt.InvalidTokenError:
            return None  # Здесь можно добавить логику обработки исключения.

        return decoded_payload

    @classmethod
    async def _create_access_token(
        cls,
        user: UserModel,
    ) -> str:
        """
        Создаёт токен доступа для пользователя.

        Args:
            user (UserModel): Модель пользователя.

        Returns:
            str: Токен доступа.
        """
        created_at: datetime = datetime.now(timezone.utc)
        exp = timedelta(seconds=ACCESS_TOKEN_EXPIRE_SECONDS)
        exp += created_at.utcnow()
        token_data: dict = {
            'sub': user.user_id,
            'iat': created_at,
            'exp': exp,
        }
        return jwt.encode(
            token_data,
            SECRET_KEY=SECRET_KEY,
            algorithms=[TOKEN_ALG],
        )

    @classmethod
    async def _create_refresh_token(
        cls,
        session: AsyncSession,
        user: UserModel,
    ) -> UUID:
        """
        Создаёт новый refresh токен для пользователя.

        Args:
            session (AsyncSession): Сессия базы данных.
            user (UserModel): Модель пользователя.

        Returns:
            UUID: UUID нового рефреш токена.
        """
        refresh_token: UUID = uuid4()
        await RefreshTokenDAO.add(session, RefreshTokenCreate(
            refresh_token=refresh_token,
            expires_in=REFRESH_TOKEN_EXPIRE_SECONDS,
            user_id=user.user_id,
        ))
        return refresh_token
