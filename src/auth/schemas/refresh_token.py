import uuid
from typing import Optional

from pydantic import BaseModel, Field


class RefreshTokenCreate(BaseModel):
    """
    Класс для создания нового объекта RefreshToken.

    Attributes:
        refresh_token (uuid.UUID): Уникальный идентификатор
        для refresh токена.
        expires_int (int): Время жизни токена в секундах.
        user_id (uuid.UUID): Уникальный идентификатор пользователя,
        связанного с этим токеном.
    """

    refresh_token: uuid.UUID
    expires_int: int
    user_id: uuid.UUID


class RefreshTokenUpdate(RefreshTokenCreate):
    """
    Класс для обновления существующего объекта RefreshToken.

    Attributes:
        refresh_token (uuid.UUID): Уникальный идентификатор для
        refresh токена.
        expires_int (int): Время жизни токена в секундах.
        user_id (Optional[int]): Уникальный идентификатор пользователя,
        связанного с этим токеном. Может быть None.
    """

    user_id: Optional[int] = Field(None)
