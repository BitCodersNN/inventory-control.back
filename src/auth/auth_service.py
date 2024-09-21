from functools import wraps
from inspect import signature
from typing import Callable, Optional

from src.auth.schemas.tokens import AccessToken, RefreshToken, Tokens
from src.auth.schemas.user import UserAuth
from src.auth.services import (
    AuthenticateService,
    LogoutService,
    RefreshService,
)
from src.auth.utils.password_manager import PasswordManager
from src.auth.utils.tokens.token_manager import TokenManager
from src.configs.token_config import (
    ACCESS_TOKEN_EXPIRE_SECONDS,
    REFRESH_TOKEN_EXPIRE_SECONDS,
    SECRET_KEY,
    TOKEN_ALG,
)
from src.utils.database_session import get_async_session


class AuthService:
    """
    Сервис аутентификации и управления токенами.

    Этот класс предоставляет методы для аутентификации пользователей,
    управления токенами доступа и обновления,
    а также для выхода из системы.

    Attributes:
        _token_manager: Менеджер токенов для правления, доступа и обновления.
        _password_manager: Менеджер паролей для проверки и хеширования паролей.
        _authenticate_service: Сервис аутентификации.
        _logout_service: Сервис выхода из системы.
        _refresh_service: Сервис обновления токенов.

    """

    def __init__(self) -> None:
        """
        Инициализирует экземпляр AuthService.

        Устанавливает менеджеры токенов и паролей, а также
               сервисы аутентификации, выхода и обновления.
        """
        self._token_manager = TokenManager(
            ACCESS_TOKEN_EXPIRE_SECONDS,
            TOKEN_ALG,
            SECRET_KEY,
            None,
        )

        self._password_manager = PasswordManager()

        self._authenticate_service = AuthenticateService(
            self._token_manager,
            self._password_manager,
            REFRESH_TOKEN_EXPIRE_SECONDS,
        )

        self._logout_service = LogoutService(
            self._token_manager,
        )

        self._refresh_service = RefreshService(
            self._token_manager,
        )

    async def authenticate(
        self,
        user_auth: UserAuth,
    ) -> Optional[Tokens]:
        """
        Аутентифицирует пользователя и возвращает токены доступа и обновления.

        Args:
            user_auth (UserAuth): Данные аутентификации пользователя.

        Returns:
            Optional[Tokens]: Токены доступа и обновления,
                если аутентификация прошла успешно, иначе None.
        """
        return await self._session_connect(
            self._authenticate_service.authenticate,
            user_auth,
        )

    async def logout(
        self,
        refresh_token: RefreshToken,
    ) -> Optional[Tokens]:
        """
        Выполняет выход пользователя из системы.

        Args:
            refresh_token (RefreshToken): Токен обновления
                                    для выхода из системы.

        Returns:
            Optional[Tokens]: Токены доступа и обновления,
                    если выход прошел успешно, иначе None.
        """
        return await self._session_connect(
            self._logout_service.logout,
            refresh_token,
        )

    async def logout_from_all_devices(
        self,
        access_token: AccessToken,
    ) -> Optional[Tokens]:
        """
        Выполняет выход пользователя из системы со всех устройств.

        Args:
            access_token (AccessToken): Токен доступа для
                                выхода со всех устройств.

        Returns:
            Optional[Tokens]: Токены доступа и обновления,
                    если выход прошел успешно, иначе None.
        """
        return await self._session_connect(
            self._logout_service.logout_from_all_devices,
            access_token,
        )

    async def refresh(
        self,
        refresh_token: RefreshToken,
    ) -> Optional[Tokens]:
        """
        Обновляет токены доступа и обновления, используя токен обновления.

        Args:
            refresh_token (RefreshToken): Токен обновления
                                    для обновления токенов.

        Returns:
            Optional[Tokens]: Новые токены доступа и обновления,
                    если обновление прошло успешно, иначе None.
        """
        return await self._session_connect(
            self._refresh_service.refresh,
            refresh_token,
        )

    def identification(
        self,
        func: Callable,
    ) -> Callable:
        """
        Декоратор для идентификации пользователя по токену доступа.

        Args:
            func (Callable): Функция, которую нужно декорировать.

        Returns:
            Callable: Декорированная функция.

        Raises:
            KeyError: Если токен доступа отсутствует в kwargs.
        """
        @wraps(func)
        def ind_decorate(*args, **kwargs):  # noqa: WPS430
            arg_name: str = 'access_token'
            func_args: dict = dict(signature(func).parameters)

            if arg_name not in func_args:
                raise KeyError('access_token отсутствует в kwargs')

            args_position: int = list(func_args.keys()).index(arg_name)
            access_token: str = args[args_position]
            self._token_manager.decode_token(access_token)

            return func(*args, **kwargs)
        return ind_decorate

    @classmethod
    async def _session_connect(cls, func: Callable, *args, **kwargs):
        """
         Выполняет функцию в а синхронной сессией базы данных.

        Args:
            func (Callable): Функция, выполняемая в контексте сессии.
            args: Аргументы для переданной функции.
            kwargs: Ключевые аргументы для переданной функции.

        Returns:
            Any: Результат выполнения переданной функции.
        """
        async with get_async_session() as session:
            func_result = await func(session, *args, **kwargs)
            await session.commit()
        return func_result
