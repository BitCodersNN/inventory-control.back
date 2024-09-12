from abc import ABC, abstractmethod
from datetime import datetime, timedelta, timezone
from uuid import UUID, uuid4

from jose import jwt

from src.auth.models import UserModel


class TokenStrategy(ABC):
    """
    Абстрактный класс для создания и декодирования токенов доступа и обновления.

    Methods:
        create_access_token: Создает токен доступа для указанного пользователя.
        create_refresh_token: Создает новый токен обновления.
        decode_token: Абстрактный метод для декодирования токена доступа.
    """

    def __init__(
        self,
        access_token_expire_seconds: int,
        secret_key: str,
        algorithm_name: str,
    ):
        """
        Инициализация класса TokenStrategy.

        Args:
            access_token_expire_seconds (int): Время жизни токена доступа
            в секундах.
            secret_key (str): Секретный ключ, используемый для подписи токенов.
            algorithm_name (str): Название алгоритма, используемого
            для подписи токенов.
        """
        self._access_token_expire_seconds = access_token_expire_seconds
        self._secret_key = secret_key
        self._algorithm_name = algorithm_name

    def create_access_token(
        self,
        user: UserModel,
    ) -> str:
        """
        Создает токен доступа для указанного пользователя.

        Args:
            user (UserModel): Объект пользователя, для которого создается токен.

        Returns:
            str: Сгенерированный токен доступа.
        """
        created_at: datetime = datetime.now(timezone.utc)
        exp = timedelta(seconds=self._access_token_expire_seconds)
        exp += created_at
        token_data: dict = {
            'sub': user.user_id,
            'iat': created_at,
            'exp': exp,
        }
        return jwt.encode(
            token_data,
            key=self._secret_key,
            algorithm=self._algorithm_name,
        )

    def create_refresh_token(self) -> UUID:
        """
        Создает новый токен обновления.

        Returns:
            UUID: Уникальный идентификатор токена обновления.
        """
        return uuid4()

    @abstractmethod
    def decode_token(self, access_token: str) -> dict:
        """
        Абстрактный метод для декодирования токена доступа.

        Args:
            access_token (str): Токен доступа, который нужно декодировать.

        Returns:
            dict: Декодированные данные токена.
        """
