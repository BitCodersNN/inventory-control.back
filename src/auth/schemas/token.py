import uuid

from pydantic import BaseModel, Field


class Token(BaseModel):
    """
    Класс для представления объекта Token.

    Attributes:
        access_token (str): Строка, представляющая access токен.
        refresh_token (uuid.UUID): Уникальный идентификатор для refresh токена.
        token_type (str): Тип токена (например, 'Bearer').
    """

    access_token: str
    refresh_toke: uuid.UUID
    token_type: str = Field('Bearer')
