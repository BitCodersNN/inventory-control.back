import uuid
from typing import Optional, Union

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


class AccessTokenConfig(BaseModel):
    """
    Настройки конфигурации для токенов доступа.

    Attributes:
        access_token_expire_seconds (int): Количество секунд до истечения
        срока действия токена доступа.
        algorithm_name (str): Название алгоритма, используемого
        для шифрования токена.
        algorithm_type (str): Тип алгоритма, используемого
        для шифрования токена.
        verification_key (Optional[Union[dict, str]]): Ключ, используемый
        для проверки токена. Может быть как словарём, так и строкой.
        secret_key (str): Секретный ключ, используемый для шифрования
        и расшифровки токена.
    """

    access_token_expire_seconds: int
    algorithm_name: str
    algorithm_type: str
    verification_key: Optional[Union[dict, str]]
    secret_key: str
