from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa

from .jwt_key_generator import IJWTKeyGenerator


class AsymmetricJWTKeyGenerator(IJWTKeyGenerator):
    """
    Генератор асимметричных ключей JWT.

    Этот класс реализует интерфейс IJWTKeyGenerator
    для генерации асимметричных ключей JWT.
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
        Генерирует асимметричные ключи JWT.

        Returns:
            dict[str, bytes]: Словарь, содержащий приватный ключ 'secret_key'
            и публичный ключ 'public_key' в формате PEM.
        """
        private_key = rsa.generate_private_key(
            public_exponent=self.public_exponent,
            key_size=self.key_size,
            backend=default_backend(),
        )

        private_pem = private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption(),
        )

        public_key = private_key.public_key()

        public_pem = public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo,
        )

        return {
            'secret_key': private_pem,
            'public_key': public_pem,
        }
