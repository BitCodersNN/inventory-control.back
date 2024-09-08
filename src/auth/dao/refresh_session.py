from src.auth.models import RefreshSessionModel
from src.auth.schemas.refresh_session import (
    RefreshSessionCreate,
    RefreshSessionUpdate,
)
from src.utils.base_dao import BaseDAO


class RefreshSessionDAO(
    BaseDAO[RefreshSessionModel, RefreshSessionCreate, RefreshSessionUpdate],
):
    """
    Объект доступа к данным для модели RefreshSessionModel.

    Этот класс наследуется от BaseDAO и предоставляет методы для выполнения
    операций CRUD (создание, чтение, обновление, удаление)
    над объектами модели RefreshTokenModel.

    Attributes:
        model (RefreshTokenModel): Модель данных, с которой работает DAO.
    """

    model = RefreshSessionModel
