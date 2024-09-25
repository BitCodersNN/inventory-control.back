import uuid

from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.dao.refresh_session import RefreshSessionDAO
from src.auth.schemas.access_token_payload import AccessTokenPayload
from src.auth.schemas.tokens import AccessToken, RefreshToken
from src.auth.utils.exceptions import RefreshNotExistError, UnexpectedError
from src.auth.utils.tokens.token_manager import TokenManager


class LogoutService:
    """
    Сервис выхода пользователя из системы.

    Этот класс предоставляет методы для выхода пользователя из системы,
                        используя токен обновления или токен доступа.

    Attributes:
        _token_manager (TokenManager): Менеджер токенов
                            для декодирования токенов.
    """

    def __init__(
        self,
        token_manager: TokenManager,
    ):
        """
        Инициализирует экземпляр LogoutService.

        Args:
            token_manager (TokenManager): Менеджер токенов
                                для декодирования токенов.
        """
        self._token_manager = token_manager

    async def logout(
        self,
        session: AsyncSession,
        refresh_token: RefreshToken,
    ):
        """
        Выполняет выход пользователя из системы, используя токен обновления.

        Args:
            session (AsyncSession): Асинхронная сессия базы данных.
            refresh_token (RefreshToken): Рефрешь токен.

        Returns:
            int: Количество удаленных сессий.

        Raises:
            RefreshNotExistError: Если токен обновления не существует.
            UnexpectedError: Если произошла неожиданная ошибка.
        """
        count: int = await RefreshSessionDAO.delete(
            session,
            refresh_token=refresh_token,
        )
        if count == 0:
            raise RefreshNotExistError
        elif count is None:
            raise UnexpectedError

        return count

    async def logout_from_all_devices(
        self,
        session: AsyncSession,
        access_token: AccessToken,
    ):
        """
        Выполняет выход пользователя из системы со всех устройств.

        Args:
            session (AsyncSession): Асинхронная сессия базы данных.
            access_token (AccessToken): Акцессс токен.

        Returns:
            int: Количество удаленных сессий.

        Raises:
            RefreshNotExistError: Если токен обновления не существует.
            UnexpectedError: Если произошла неожиданная ошибка.
        """
        payload: AccessTokenPayload = await self._token_manager.decode_token(
            access_token.access_token,
        )
        user_id: uuid.UUID = payload.sub
        count: int = await RefreshSessionDAO.delete(
            session,
            user_id=user_id,
        )
        if count == 0:
            raise RefreshNotExistError
        elif count is None:
            raise UnexpectedError

        return count
