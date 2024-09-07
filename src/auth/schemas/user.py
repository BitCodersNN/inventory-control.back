import uuid
from typing import Optional

from pydantic import BaseModel, Field

from src.auth.models import UserRoles
from src.auth.models.users import MAX_LOGIN_SIZE, MAX_NAME_SIZE


class _UserBase(BaseModel):
    """
    Базовая модель пользователя.

    Атрибуты:
        login (Optional[str]): Логин пользователя.
        name (Optional[str]): Имя пользователя.
        role (UserRoles): Роль пользователя. По умолчанию - читатель.
    """

    login: Optional[str] = Field(None, max_length=MAX_LOGIN_SIZE)
    name: Optional[str] = Field(None, max_length=MAX_NAME_SIZE)
    role: UserRoles = Field(UserRoles.reader)


class UserCreate(_UserBase):
    """
    Модель для создания нового пользователя.

    Атрибуты:
        login (str): Логин пользователя.
        name (str): Имя пользователя.
        password (str): Пароль пользователя.
        role (UserRoles): Роль пользователя. По умолчанию - читатель.
    """

    login: str
    name: str
    password: str


class UserUpdate(_UserBase):
    """
    Модель для обновления данных пользователя.

    Атрибуты:
        login (Optional[str]): Логин пользователя.
        name (Optional[str]): Имя пользователя.
        role (UserRoles): Роль пользователя. По умолчанию - читатель.
        password (Optional[str]): Новый пароль пользователя.
    """

    password: Optional[str] = Field(None)


class User(_UserBase):
    """
    Модель пользователя.

    Атрибуты:
        user_id (uuid.UUID): Уникальный идентификатор пользователя.
        login (str): Логин пользователя.
        name (str): Имя пользователя.
        role (UserRoles): Роль пользователя.
    """

    user_id: uuid.UUID
    login: str
    name: str
    role: UserRoles

    class Config:
        """
        Конфигурация модели.

        Атрибуты:
            from_orm (bool): Флаг для использования ORM-совместимости.
        """

        from_orm = True


class UserCreateDB(_UserBase):
    """
    Модель для создания нового пользователя в базе данных.

    Атрибуты:
        login (str): Логин пользователя.
        name (str): Имя пользователя.
        role (UserRoles): Роль пользователя. По умолчанию - читатель.
        pass_hash (str): Хеш пароля пользователя.
    """

    login: str
    name: str
    pass_hash: str


class UserUpdateDB(_UserBase):
    """
    Модель для обновления данных пользователя в базе данных.

    Атрибуты:
        login (Optional[str]): Логин пользователя.
        name (Optional[str]): Имя пользователя.
        role (UserRoles): Роль пользователя. По умолчанию - читатель.
        pass_hash (Optional[str]): Новый хеш пароля пользователя.
    """

    pass_hash: Optional[str] = Field(None)
