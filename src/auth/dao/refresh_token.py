from src.auth.models import RefreshTokenModel
from src.base_dao import BaseDAO


class RefreshTokenDAO(BaseDAO[RefreshTokenModel]):
    """
    Объект доступа к данным для модели RefreshTokenModel.

    Этот класс наследуется от BaseDAO и предоставляет методы для выполнения
    операций CRUD (создание, чтение, обновление, удаление)
    над объектами модели RefreshTokenModel.

    Атрибуты:
        model (RefreshTokenModel): Модель данных, с которой работает DAO.
    """

    model = RefreshTokenModel
