from uuid import UUID

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.auth_service import AuthService
from src.auth.schemas.token import Token
from src.auth.schemas.user import UserAuth

router = APIRouter()
auth_service = AuthService()
async_session = AsyncSession()
oauth2_scheme = Depends(OAuth2PasswordBearer(tokenUrl='token'))


@router.get('/authenticate')
def authenticate(
    auth_user: UserAuth,
):
    """
    Аутентифицирует пользователя.

    Args:
        auth_user: Данные пользователя для аутентификации.

    Returns:
        Результат аутентификации.
    """
    return auth_service.authenticate(async_session, auth_user)


@router.get('/logout')
@auth_service.identification
def logout(
    refresh_token: UUID,
    access_token: str = oauth2_scheme,
):
    """
    Выход пользователя из системы.

    Args:
        refresh_token: Refresh token пользователя.
        access_token: Access token пользователя.

    Returns:
        Результат выхода из системы.
    """
    token: Token = Token(access_token=access_token, refresh_token=refresh_token)
    return auth_service.logout(async_session, token)


@router.get('/logout_from_all_devices')
def logout_from_all_devices(
    refresh_token: UUID,
    access_token: str = oauth2_scheme,
):
    """
    Выход пользователя из системы со всех устройств.

    Args:
        refresh_token: Refresh token пользователя.
        access_token: Access token пользователя.

    Returns:
        Результат выхода из системы со всех устройств.
    """
    token: Token = Token(access_token=access_token, refresh_token=refresh_token)
    return auth_service.logout_from_all_devices(async_session, token)


@router.get('/refresh')
def refresh(
    refresh_token: UUID,
    access_token: str = oauth2_scheme,
):
    """
    Обновляет access token пользователя.

    Args:
        refresh_token: Refresh token пользователя.
        access_token: Access token пользователя.

    Returns:
        Новый access token.
    """
    token: Token = Token(access_token=access_token, refresh_token=refresh_token)
    return auth_service.refresh(async_session, token)
