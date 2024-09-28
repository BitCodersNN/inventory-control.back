import abc


class IJWTKeyGenerator(abc.ABC):
    """
    Абстрактный базовый класс для генераторов ключей JWT.

    Этот класс определяет интерфейс для генерации ключей JWT.
    """

    @abc.abstractmethod
    def generate_keys(self) -> dict[str, bytes]:
        """
        Генерирует ключи JWT.

        Returns:
            dict[str, bytes]: Словарь, содержащий ключи JWT
                и их значения в виде байтов.
        """
