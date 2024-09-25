from pydantic import BaseModel


class AccessTokenPayload(BaseModel):
    """
    Модель для представления полезной нагрузки JWT.

    Атрибуты:
        sub (str): Идентификатор пользователя.
    """

    sub: str
