from typing import Optional

from passlib.context import CryptContext


class PasswordManager:
    """
    Управление паролями и их хешированием.

    Используется билблиотека CryptContext.

    Attributes:
        _default_crypt_context (CryptContext): Контекст шифрования
        по умолчанию, использующий схему 'bcrypt'

    Methods:
        is_valid_password: Проверяет, соответствует ли открытый пароль
        хешированному паролю.
        get_password_hash: Генерирует хеш открытого пароля.
    """

    _default_crypt_context = CryptContext(
        schemes=['bcrypt'],
        deprecated='auto',
    )

    def __init__(
        self,
        pwd_context: Optional[CryptContext] = None,
    ):
        """
        Инициализация объекта PasswordManager.

        Args:
            pwd_context (Optional[CryptContext]): Опциональный объект
            CryptContext для шифрования паролей. Если не указан,
            будет использоваться контекст по умолчанию.
        """
        self.pwd_context = pwd_context or self._default_crypt_context

    def is_valid_password(
        self,
        plain_password: str,
        hashed_password: str,
    ) -> bool:
        """
        Проверяет, соответствует ли открытый пароль хешированному паролю.

        Args:
            plain_password (str): Открытый пароль, который нужно проверить.
            hashed_password (str): Хешированный пароль, с которым нужно
            сравнить открытый пароль.

        Returns:
            bool: True, если открытый пароль соответствует хешированному
            паролю, иначе False.
        """
        return self.pwd_context.verify(
            plain_password,
            hashed_password,
        )

    def get_password_hash(
        self,
        password: str,
    ) -> str:
        """
        Генерирует хеш открытого пароля.

        Args:
            password (str): Открытый пароль, для которого генерируется хеш.

        Returns:
            str: Хеш открытого пароля.
        """
        return self.pwd_context.hash(password)
