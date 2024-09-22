import uuid

from pydantic import BaseModel, Field


class Tokens(BaseModel):
    """
    Класс для представления объекта Token.

    Attributes:
        access_token (str): Строка, представляющая access токен.
        refresh_token (uuid.UUID): Уникальный идентификатор для refresh токена.
        token_type (str): Тип токена (например, 'Bearer').
    """

    access_token: str
    refresh_token: uuid.UUID
    token_type: str = Field('Bearer')


class RefreshToken(BaseModel):
    """
    Класс для представления объекта RefreshToken.

    Attributes:
        refresh_token (uuid.UUID): Уникальный
            идентификатор для refresh токена.
    """

    refresh_token: uuid.UUID


class AccessToken(BaseModel):
    """
    Класс для представления объекта AccessToken.

    Attributes:
        access_token (str): Строка,представляющая access токен.
    """

    access_token: str
