from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.dao.refresh_session import RefreshSessionDAO
from src.auth.dao.user import UserDAO
from src.auth.models import UserModel
from src.auth.schemas.refresh_session import RefreshSessionCreate
from src.auth.schemas.tokens import Tokens
from src.auth.schemas.user import UserAuth
from src.auth.utils.exceptions import InvalidCredentialsError
from src.auth.utils.password_manager import PasswordManager
from src.auth.utils.tokens.token_manager import TokenManager


class AuthenticateService:
    """
    Сервис аутентификации пользователей.

    Этот класс предоставляет метод для аутентификации
    пользователей и создания токенов доступа и обновления.

    Attributes:
        _token_manager (TokenManager): Менеджер токенов для
                                создания и управления токенами.
        _password_manager (PasswordManager): Менеджер паролей для
                                                проверки паролей.
        _refresh_token_expire_seconds (int): Время жизни токена
                                        обновления в секундах.
    """

    def __init__(
        self,
        token_manager: TokenManager,
        password_manager: PasswordManager,
        refresh_token_expire_seconds: int,
    ):
        """
        Инициализирует экземпляр AuthenticateService.

        Args:
            token_manager (TokenManager): Менеджер токенов для
                                создания и управления токенами.
            password_manager (PasswordManager): Менеджер паролей
                                            для проверки паролей.
            refresh_token_expire_seconds (int): Время жизни
                                токена обновления в секундах.
        """
        self._token_manager = token_manager
        self._password_manager = password_manager
        self._refresh_token_expire_seconds = refresh_token_expire_seconds

    async def authenticate(
        self,
        session: AsyncSession,
        user_auth: UserAuth,
    ) -> Optional[Tokens]:
        """
        Аутентифицирует пользователя и возвращает токены.

        Args:
            session (AsyncSession): Асинхронная сессия базы данных.
            user_auth (UserAuth): Данные аутентификации пользователя.

        Returns:
            Optional[Tokens]: Токены доступа и обновления,
            если аутентификация прошла успешно, иначе None.

        Raises:
            InvalidCredentialsError: Если предоставленные
                                    учетные данные неверны.
        """
        user: Optional[UserModel] = await UserDAO.find_one_or_none(
            session,
            login=user_auth.login,
        )

        if user is None:
            raise InvalidCredentialsError

        conditions: bool = self._password_manager.compare(
            user_auth.password,
            user.pass_hash,
        )

        if not conditions:
            raise InvalidCredentialsError

        token: Tokens = self._token_manager.create_token(user.user_id)
        await RefreshSessionDAO.add(
            session,
            RefreshSessionCreate(
                refresh_token=token.refresh_token,
                expires_in=self._refresh_token_expire_seconds,
                user_id=user.user_id,
            ),
        )
        return token
