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
    User authentication service.

    Methods:
        authenticate: Validates user credentials and returns tokens.
        identification: Decorator for token validation.
        refresh: Creates a new access token for a user.
        logout: Removes the refresh token for a user.
        logout_from_all_devices: Removes all refresh tokens for a user.
    """

    def __init__(self) -> None:
        """Инициализация класса TokenFacade."""
        self.token_manager = TokenManager(
            ACCESS_TOKEN_EXPIRE_SECONDS,
            TOKEN_ALG,
            SECRET_KEY,
            None
        )

    async def authenticate(
        self,
        session: AsyncSession,
        user_auth: UserAuth,
    ) -> Optional[Token]:
        """
        Validates user credentials and generates tokens.

        Args:
            session: Async session for DB operations.
            user_auth: User credentials (login and password).

        Returns:
            Optional[Token]: Token object with access and
                                    refresh tokens or None.
        """
        user: Optional[UserModel] = await UserDAO.find_one_or_none(
            session,
            UserModel.login == user_auth.login,
        )

        if user is None:  # Check if user exists
            return None

        if not PasswordManager().compare(user_auth.password, user.pass_hash):
            return None  # Invalid password

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
        Decorator to check access token validity.

        Args:
            func: Function to decorate.

        Returns:
            Callable: Wrapped function with token validation.
        """

        @wraps(func)
        def ind_decorate(*args, **kwargs):  # noqa: WPS430
            access_token = kwargs.get('access_token')
            if not access_token:
                raise KeyError('access_token is missing in kwargs')
            if not isinstance(access_token, str):
                raise ValueError('access_token must be a string')
            return self._verify_token(access_token)

        return ind_decorate

    async def refresh(
        self,
        session: AsyncSession,
        token: Token,
    ) -> Optional[Token]:
        """
        Creates a new access token for a user.

        Args:
            session: Async session for DB operations.
            token: Token to validate for creating a new access token.

        Returns:
            Optional[Token]: New Token object or None if invalid.
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
        Removes all refresh tokens for a user.

        Args:
            token: User access token for identification.
            session: Async session for DB operations.
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
        Checks if the access token is valid.

        Args:
            access_token: Token to validate.

        Returns:
            bool: True if valid, False otherwise.
        """
        return self.token_manager.decode_token(access_token) is not None
