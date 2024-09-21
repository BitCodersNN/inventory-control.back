from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.dao.refresh_session import RefreshSessionDAO
from src.auth.dao.user import UserDAO
from src.auth.models import RefreshSessionModel, UserModel
from src.auth.schemas.refresh_session import RefreshSessionUpdate
from src.auth.schemas.tokens import RefreshToken, Tokens
from src.auth.utils.exceptions import (
    InvalidCredentialsError,
    InvalidRefreshTokenError,
)
from src.auth.utils.tokens.token_manager import TokenManager


class RefreshService:
    """
    Сервис обновления токенов доступа и обновления.

    Этот класс предоставляет метод для обновления токенов.

    Attributes:
        _token_manager (TokenManager): Менеджер токенов для создания и
        управления токенами.
    """

    def __init__(
        self,
        token_manager: TokenManager,
    ):
        """
        Инициализирует экземпляр RefreshService.

        Args:
            token_manager (TokenManager): Менеджер токенов для
                                создания и управления токенами.
        """
        self._token_manager = token_manager

    async def refresh(
        self,
        session: AsyncSession,
        refresh_token: RefreshToken,
    ) -> Optional[Tokens]:
        """
        Обновляет токены доступа и обновления, используя токен обновления.

        Args:
            session (AsyncSession): Асинхронная сессия базы данных.
            refresh_token (RefreshToken): Рефрешь токен.

        Returns:
            Optional[Tokens]: Новые токены доступа и обновления,
                    если обновление прошло успешно, иначе None.

        Raises:
            InvalidRefreshTokenError: Если токен обновления недействителен.
            InvalidCredentialsError: Если пользователь не найден.
        """
        refresh_session: Optional[RefreshSessionModel]
        refresh_session = await RefreshSessionDAO.find_one_or_none(
            session,
            refresh_token=refresh_token,
        )
        if refresh_session is None:
            raise InvalidRefreshTokenError

        user: Optional[UserModel] = await UserDAO.find_one_or_none(
            session,
            user_id=refresh_session.user_id,
        )
        if user is None:
            raise InvalidCredentialsError

        token: Tokens = self._token_manager.create_token(
            refresh_session.user_id,
        )
        await RefreshSessionDAO.update(
            session,
            RefreshSessionModel.token_id == refresh_session.token_id,
            obj_in=RefreshSessionUpdate(
                refresh_token=token.refresh_token,
            ),
        )
        return token
