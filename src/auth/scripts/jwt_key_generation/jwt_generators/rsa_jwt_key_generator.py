from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric.rsa import (
    RSAPrivateKey,
    generate_private_key,
)

from .asymmetric_jwt_key_generator import IAsymmetricJWTKeyGenerator


class RsaJWTKeyGenerator(IAsymmetricJWTKeyGenerator):
    """
    Класс для генерации асимметричных ключей JWT на основе RSA.

    Args:
        public_exponent (int): Публичная экспонента для генерации ключей.
            По умолчанию: 65537.
        key_size (int): Размер ключа в битах.
            По умолчанию: 2048.
    """

    def __init__(
        self,
        public_exponent: int = 65537,
        key_size: int = 2048,
    ):
        """
        Инициализирует генератор асимметричных ключей JWT.

        Args:
            public_exponent (int): Публичная экспонента для генерации ключей.
                По умолчанию: 65537.
            key_size (int): Размер ключа в битах.
                По умолчанию: 2048.
        """
        self.public_exponent = public_exponent
        self.key_size = key_size

    def generate_keys(self) -> dict[str, bytes]:
        """
        Генерирует пару ключей (публичный и закрытый) для JWT.

        Returns:
            dict[str, bytes]: Словарь, содержащий публичный и закрытый ключи.
        """
        return self._generate_key(self._generate_private_key())

    def _generate_private_key(self) -> RSAPrivateKey:
        """
        Генерирует закрытый RSA-ключ.

        Returns:
            RSAPrivateKey: Сгенерированный закрытый RSA-ключ.
        """
        return generate_private_key(
            public_exponent=self.public_exponent,
            key_size=self.key_size,
            backend=default_backend(),
        )
