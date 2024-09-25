import abc

from cryptography.hazmat.primitives import serialization

from .jwt_key_generator import IJWTKeyGenerator


class IAsymmetricJWTKeyGenerator(IJWTKeyGenerator, abc.ABC):
    """
    Абстрактный базовый класс для генераторов асимметричных ключей JWT.

    Этот класс расширяет интерфейс IJWTKeyGenerator
    и предоставляет абстрактный метод для генерации закрытого ключа,
    а также метод для генерации пары ключей (закрытый и публичный).
    """

    @abc.abstractmethod
    def _generate_private_key(self):
        """
        Абстрактный метод для генерации закрытого ключа.

        Returns:
            RSAPrivateKey: Сгенерированный закрытый ключ.
        """

    def _generate_key(self, private_key) -> dict[str, bytes]:
        """
        Генерирует пару ключей (закрытый и публичный) на основе закрытого ключа.

        Args:
            private_key: Закрытый ключ, сгенерированный
                методом _generate_private_key.

        Returns:
            dict[str, bytes]: Словарь, содержащий закрытый
                и публичный ключи в формате PEM.
        """
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
