import uuid
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class _RefreshSessionBase(BaseModel):
    """
    Базовый класс для сессии обновления токена.

    Attributes:
        refresh_token (Optional[uuid.UUID]): UUID обновляющего токена.
        expires_in (Optional[int]): Время жизни токена.
        По умолчанию - False.
        user_id (Optional[uuid.UUID]): UUID пользователя, связанного с сессией.
    """

    refresh_token: Optional[uuid.UUID] = Field(None)
    expires_in: Optional[int] = Field(None)
    user_id: Optional[uuid.UUID] = Field(None)


class RefreshSessionCreate(_RefreshSessionBase):
    """
    Класс для создания новой сессии обновления токена.

    Attributes:
        refresh_token (uuid.UUID): UUID обновляющего токена.
        expires_in (int): Время жизни токена.
        user_id (uuid.UUI): UUID пользователя, связанного с сессией.
        По умолчанию - False.
    """

    refresh_token: uuid.UUID
    expires_in: int
    user_id: uuid.UUID


class RefreshSessionUpdate(_RefreshSessionBase):
    """
    Класс для обновления существующей сессии обновления токена.

    Attributes:
        refresh_token (uuid.UUID): UUID обновляющего токена.
        expires_in (Optional[int]): Время жизни токена.
        По умолчанию - False.
        user_id (Optional[uuid.UUID]): UUID пользователя, связанного с сессией.
        created_at (datetime): Время создания токена
    """

    refresh_token: uuid.UUID
    created_at: datetime
