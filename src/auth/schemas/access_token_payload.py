import uuid

from pydantic import BaseModel


class AccessTokenPayload(BaseModel):
    """
    Модель для представления полезной нагрузки JWT.

    Атрибуты:
        sub (uuid.UUID): Идентификатор пользователя.
    """

    sub: uuid.UUID
