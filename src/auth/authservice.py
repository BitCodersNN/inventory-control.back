from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.dao.refresh_session import RefreshSessionDAO
from src.auth.dao.user import UserDAO
from src.auth.models import RefreshSessionModel, UserModel
from src.auth.schemas.refresh_session import RefreshSessionCreate
from src.auth.schemas.token import Token
from src.auth.schemas.user import UserAuth
from src.auth.utils.password_manager import PasswordManager
from src.auth.utils.token_manager import TokenManager
from src.configs.token_config import REFRESH_TOKEN_EXPIRE_SECONDS


class AuthService:
    """
    Служба аутентификации пользователя.

    Methods:
        authenticate: Проверяет подлинность пользователя,
                      возвращая токены, если учетные данные верны.

        identification: Проверяет действительность токена доступа.

        create_token: Создает новый токен доступа для пользователя.

        logout: Удаляет токен обновления для заданного пользователя.

        logout_from_all_devices: Удаляет все токены обновления
                                 для заданного пользователя.
    """

    @classmethod
    async def authenticate(
        cls,
        session: AsyncSession,
        user_auth: UserAuth,
    ) -> Optional[Token]:
        """
        Проверяет подлинность пользователя по учетным данным и создает токены.

        Args:
            session (AsyncSession): Асинхронная сессия для работы с БД.
            user_auth (UserAuth): Учетные данные пользователя (логин и пароль).

        Returns:
            Optional[Token]: Возвращает объект Token, содержащий
                             токены доступа и обновления, или None,
                             если аутентификация не удалась.
        """
        user: Optional[UserModel] = await UserDAO.find_one_or_none(
            session,
            UserModel.login == user_auth.login,
        )
        if not user:
            return None

        if PasswordManager().compare(user_auth.password, user.pass_hash):
            token: Token = TokenManager.create_tokens(user)
            await RefreshSessionDAO.add(
                session,
                RefreshSessionCreate(
                    refresh_token=token.refresh_token,
                    expires_in=REFRESH_TOKEN_EXPIRE_SECONDS,
                    user_id=user.user_id,
                ),
            )
            return token
        return None

    @classmethod
    def identification(
        cls,
        token: Token,
    ) -> bool:
        """
        Проверяет действительность токена доступа.

        Args:
            token (Token): Токен, который необходимо проверить.

        Returns:
            bool: Возвращает True, если токен действителен,
                  иначе False.
        """
        return bool(TokenManager.decode_token(token.access_token))

    @classmethod
    async def create_token(
        cls,
        session: AsyncSession,
        user_id: int,
    ) -> Optional[Token]:
        """
        Создает новый токен доступа для указанного пользователя.

        Args:
            session (AsyncSession): Асинхронная сессия для работы с БД.

            user_id (int): Идентификатор пользователя, для
                           которого создается токен.

        Returns:
            Optional[Token]: Возвращает новый объект Token, или
                             None, если пользователь не найден.
        """
        user: Optional[UserModel] = await UserDAO.find_one_or_none(
            session,
            UserModel.user_id == user_id,
        )
        if not user:
            return None
        return TokenManager.create_tokens(user)

    @classmethod
    async def logout(
        cls,
        session: AsyncSession,
        token: Token,
    ):
        """
        Удаляет токен обновления для заданного пользователя.

        Args:
            session (AsyncSession): Асинхронная сессия для работы с БД.
            token (Token): Токен доступа пользователя.
        """
        await RefreshSessionDAO.delete(
            session,
            RefreshSessionModel.refresh_token == token.refresh_token,
        )

    @classmethod
    async def logout_from_all_devices(
        cls,
        token: Token,
        session: AsyncSession,
    ):
        """
        Удаляет все токены обновления для заданного пользователя.

        Args:
            token (Token): Токен доступа пользователя для
                           идентификации.

            session (AsyncSession): Асинхронная сессия для работы с БД.
        """
        user_id: int = await TokenManager.decode_token(
            token.access_token,
        )['sub']
        await RefreshSessionDAO.delete(
            session,
            RefreshSessionModel.user_id == user_id,
        )
