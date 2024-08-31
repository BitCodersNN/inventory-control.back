from src.auth.models import UserModel
from src.auth.schemas.user import UserCreateDB, UserUpdateDB
from src.utils.base_dao import BaseDAO


class UserDAO(BaseDAO[UserModel, UserCreateDB, UserUpdateDB]):
    """
    Объект доступа к данным для модели UserModel.

    Этот класс наследуется от BaseDAO и предоставляет методы для выполнения
    операций CRUD (создание, чтение, обновление, удаление)
    над объектами модели UserModel.

    Атрибуты:
        model (UserModel): Модель данных, с которой работает DAO.
    """

    model = UserModel
