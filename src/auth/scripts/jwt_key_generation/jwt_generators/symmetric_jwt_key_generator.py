import os

from .jwt_key_generator import IJWTKeyGenerator


class SymmetricJWTKeyGenerator(IJWTKeyGenerator):
    """
    Генератор симметричных ключей JWT.

    Этот класс реализует интерфейс IJWTKeyGenerator
    для генерации симметричных ключей JWT.
    """

    def __init__(self, key_length: int = 32):
        """
        Инициализирует генератор симметричных ключей JWT.

        Args:
            key_length (int): Длина генерируемого ключа в байтах.
            По умолчанию: 32.
        """
        self.key_length = key_length

    def generate_keys(self) -> dict[str, bytes]:
        """
        Генерирует симметричный ключ JWT.

        Returns:
            dict[str, bytes]: Словарь, содержащий один ключ 'secret_key'
            и его значение в виде байтов.
        """
        return {'secret_key': os.urandom(self.key_length)}
