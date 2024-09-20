from functools import wraps
from typing import Callable, Optional
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.dao.refresh_session import RefreshSessionDAO
from src.auth.dao.user import UserDAO
from src.auth.models import RefreshSessionModel, UserModel
from src.auth.schemas.refresh_session import (
    RefreshSessionCreate,
    RefreshSessionUpdate,
)
from src.auth.schemas.token import Token
from src.auth.schemas.user import UserAuth
from src.auth.utils.password_manager import PasswordManager
from src.auth.utils.tokens.token_manager import TokenManager
from src.configs.token_config import (
    ACCESS_TOKEN_EXPIRE_SECONDS,
    REFRESH_TOKEN_EXPIRE_SECONDS,
    SECRET_KEY,
    TOKEN_ALG,
)


class AuthService:
    """
    Сервис аутентификации пользователей.

    Methods:
        authenticate: Проверяет учетные данные пользователя и возвращает токены.
        identification: Декоратор для проверки валидности токена.
        refresh: Создает новый access token для пользователя.
        logout: Удаляет refresh token для пользователя.
        logout_from_all_devices: Удаляет все refresh token для пользователя.
    """

    def __init__(self) -> None:
        """Инициализация класса TokenFacade."""
        self.token_manager = TokenManager(
            ACCESS_TOKEN_EXPIRE_SECONDS,
            TOKEN_ALG,
            SECRET_KEY,
            None,
        )

    @classmethod
    async def logout(
        cls,
        session: AsyncSession,
        token: Token,
    ):
        """
        Удаляет refresh token для пользователя.

        Args:
            session: Асинхронная сессия для операций с БД.
            token: Access token пользователя.
        """
        await RefreshSessionDAO.delete(
            session,
            RefreshSessionModel.refresh_token == token.refresh_token,
            None,
        )

    async def authenticate(
        self,
        session: AsyncSession,
        user_auth: UserAuth,
    ) -> Optional[Token]:
        """
        Проверяет учетные данные пользователя и генерирует токены.

        Args:
            session: Асинхронная сессия для операций с БД.
            user_auth: Учетные данные пользователя (логин и пароль).

        Returns:
            Optional[Token]: Объект Token с access и refresh токенами или None.
        """
        user: Optional[UserModel] = await UserDAO.find_one_or_none(
            session,
            UserModel.login == user_auth.login,
        )

        if user is None:  # Проверка наличия пользователя
            return None

        if not PasswordManager().compare(user_auth.password, user.pass_hash):
            return None  # Неверный пароль

        token: Token = self.token_manager.create_token(user.user_id)
        await RefreshSessionDAO.add(
            session,
            RefreshSessionCreate(
                refresh_token=token.refresh_token,
                expires_in=REFRESH_TOKEN_EXPIRE_SECONDS,
                user_id=user.user_id,
            ),
        )
        return token

    def identification(
        self,
        func: Callable,
    ) -> Callable:
        """
        Декоратор для проверки валидности access token.

        Args:
            func: Функция для декорирования.

        Returns:
            Callable: Обернутая функция с проверкой токена.
        """

        @wraps(func)
        def ind_decorate(*args, **kwargs):  # noqa: WPS430
            access_token = kwargs.get('access_token')
            if not access_token:
                raise KeyError('access_token отсутствует в kwargs')
            if not isinstance(access_token, str):
                raise ValueError('access_token должен быть строкой')
            return self._verify_token(access_token)

        return ind_decorate

    async def refresh(
        self,
        session: AsyncSession,
        token: Token,
    ) -> Optional[Token]:
        """
        Создает новый access token для пользователя.

        Args:
            session: Асинхронная сессия для операций с БД.
            token: Токен для проверки и создания нового access token.

        Returns:
            Optional[Token]: Новый объект Token или None, если невалидный.
        """
        user_id: UUID = await self.token_manager.decode_token(
            token.access_token,
        )['sub']
        user: Optional[UserModel] = await UserDAO.find_one_or_none(
            session,
            UserModel.user_id == user_id,
        )
        if user is None:
            return None

        refresh_session: Optional[RefreshSessionModel]
        refresh_session = await RefreshSessionDAO.find_one_or_none(
            session,
            RefreshSessionModel.refresh_token == token.refresh_token,
        )
        if refresh_session is None:
            return None

        token: Token = self.token_manager.create_token(user_id)
        await RefreshSessionDAO.update(
            session,
            RefreshSessionModel.token_id == refresh_session.token_id,
            obj_in=RefreshSessionUpdate(
                refresh_token=token.refresh_token,
            ),
        )
        return token

    async def logout_from_all_devices(
        self,
        token: Token,
        session: AsyncSession,
    ):
        """
        Удаляет все refresh token для пользователя.

        Args:
            token: Access token пользователя для идентификации.
            session: Асинхронная сессия для операций с БД.
        """
        user_id: int = await self.token_manager.decode_token(
            token.access_token,
        )['sub']
        await RefreshSessionDAO.delete(
            session,
            RefreshSessionModel.user_id == user_id,
        )

    def _verify_token(
        self,
        access_token: str,
    ) -> bool:
        """
        Проверяет валидность access token.

        Args:
            access_token: Токен для проверки.

        Returns:
            bool: True, если валидный, иначе False.
        """
        return self.token_manager.decode_token(access_token) is not None
