from datetime import datetime, timedelta, timezone
from typing import Optional
from uuid import UUID, uuid4

from jose import jwt
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.configs.token_config import (
    ACCESS_TOKEN_EXPIRE_SECONDS,
    REFRESH_TOKEN_EXPIRE_SECONDS,
    SECRET_KEY,
    TOKEN_ALG,
)
from src.auth.dao.refresh_token import RefreshTokenDAO
from src.auth.models import RefreshTokenModel, UserModel
from src.auth.schemas.refresh_token import RefreshTokenCreate
from src.auth.schemas.token import Token


class TokenManager:
    """
    Управление токенами доступа и обновления.

    Methods:
        create_tokens: Генерирует новые токены (доступа и обновления)
                       для указанного пользователя.

        refresh: Обновляет токены доступа и обновления на основе старого
                 токена обновления.

        decode_token: Декодирует токен доступа и возвращает его
                      полезную нагрузку.
    """

    @classmethod
    async def create_tokens(
        cls,
        session: AsyncSession,
        user: UserModel,
    ) -> Token:
        """
        Создаёт новые токены доступа и обновления для пользователя.

        Новый токен обновления сохранятся в БД.

        Args:
            session (AsyncSession): Асинхронная сессия для работы с БД.
            user (UserModel): Модель пользователя, для которого
            создаются токены.

        Returns:
            Token: Объект Token, содержащий токены доступа и обновления.
        """
        access_token: str = await cls._create_access_token(user)
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
        Обновляет токены на основе старого токена обновления.

        Проверяет валидность старого токена обновления и создаёт новые токены.
        Новый токен обновления сохранятся в БД.
        Старый токен обновления помечается как отозванный.

        Args:
            session (AsyncSession): Асинхронная сессия для работы с БД.
            old_refresh_token (RefreshTokenModel): Старый токен обновления.
            user (UserModel): Модель пользователя, для которого
            обновляются токены.

        Returns:
            Token: Объект Token, содержащий новые токены доступа и обновления.

        Raises:
            ValueError: Если токен обновления не соответствует пользователю
                        или устарел.
        """
        if old_refresh_token.user_id != user.user_id:
            raise ValueError('user_id != user_id')

        created_at: datetime = old_refresh_token.created_at
        expires_in: int = old_refresh_token.expires_in
        date_end: datetime = created_at + timedelta(seconds=expires_in)
        if date_end < datetime.now(timezone.utc):
            raise ValueError('Рефреш токен устарел.')

        RefreshTokenDAO.update(
            session,
            RefreshTokenModel.token_id == old_refresh_token.token_id,
            obj_in={'revoked': True},
        )

        return Token(
            access_token=await cls._create_access_token(user),
            refresh_token=await cls._create_refresh_token(session, user),
        )

    @classmethod
    async def decode_token(cls, access_token: str) -> Optional[dict]:
        """
        Декодирует токен доступа и возвращает его полезную нагрузку.

        Args:
            access_token (str): Токен доступа для декодирования.

        Returns:
            Optional[dict]: Декодированная полезная нагрузка токена
                            или None, если токен недействителен или истек.
        """
        try:
            decoded_payload = jwt.decode(
                access_token,
                SECRET_KEY,
                algorithms=[TOKEN_ALG],
            )
        except jwt.JWTError:
            return None

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
        session: AsyncSession,
        user: UserModel,
    ) -> UUID:
        """
        Создаёт новый токен обновления для пользователя и сохраняет его в БД.

        Args:
            session (AsyncSession): Асинхронная сессия для работы с БД.
            user (UserModel): Модель пользователя, для которого создаётся токен.

        Returns:
            UUID: Сгенерированный токен обновления.
        """
        refresh_token: UUID = uuid4()
        await RefreshTokenDAO.add(
            session,
            RefreshTokenCreate(
                refresh_token=refresh_token,
                expires_in=REFRESH_TOKEN_EXPIRE_SECONDS,
                user_id=user.user_id,
            ),
        )
        return refresh_token
