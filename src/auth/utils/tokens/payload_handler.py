import uuid


class PayloadHandler:
    """Класс для обработки полезной нагрузки связанной с user id."""

    @classmethod
    def create_payload(cls, user_id: uuid.UUID) -> dict:
        """
        Создает полезную нагрузку (payload) с идентификатором пользователя.

        Args:
            user_id (uuid.UUID): Идентификатор пользователя.

        Returns:
            dict: Словарь с полезной нагрузкой, содержащий идентификатор
            пользователя в строковом формате.
        """
        return {
            'sub': str(user_id),
        }

    @classmethod
    def decode_payload(cls, payload: dict) -> dict:
        """
        Извлекает и преобразует идентификатор пользователя обратно в UUID.

        Args:
            payload (dict): Словарь с полезной нагрузкой,
            содержащий идентификатор пользователя в строковом формате.

        Returns:
            uuid.UUID: Идентификатор пользователя,
            преобразованный обратно в UUID.
        """
        return {
            'sub': uuid.UUID(payload['sub']),
        }
