from src.auth.models import RefreshTokenModel
from src.auth.schemas.refresh_token import (
    RefreshTokenCreate,
    RefreshTokenUpdate,
)
from src.utils.base_dao import BaseDAO


class RefreshTokenDAO(
    BaseDAO[RefreshTokenModel, RefreshTokenCreate, RefreshTokenUpdate],
):
    """
    Объект доступа к данным для модели RefreshTokenModel.

    Этот класс наследуется от BaseDAO и предоставляет методы для выполнения
    операций CRUD (создание, чтение, обновление, удаление)
    над объектами модели RefreshTokenModel.

    Attributes:
        model (RefreshTokenModel): Модель данных, с которой работает DAO.
    """

    model = RefreshTokenModel
