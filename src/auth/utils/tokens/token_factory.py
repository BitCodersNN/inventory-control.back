import uuid
from datetime import datetime, timedelta, timezone
from typing import Union

from jose import jwt

from src.auth.schemas.token import Token


class TokenFactory:
    """
    Класс для создания токенов доступа и обновления.

    Methods:
        secret_key (property): Возвращает текущий секретный ключ.
        secret_key (setter): Устанавливает новый секретный ключ.
        create_access_token: Создает токен доступа для указанного
        пользователя.
        create_refresh_token: Создает новый токен обновления.
    """

    def __init__(
        self,
        access_token_expire_seconds: int,
        secret_key: Union[dict, str],
        algorithm_name: str,
    ):
        """
        Инициализация класса TokenFactory.

        Args:
            access_token_expire_seconds (int): Время жизни токена доступа в сек.
            secret_key (Union[dict, str]): Секретный ключ, используемый
            для подписи токенов.
            algorithm_name (str): Название алгоритма, подписывающего токены.
        """
        self._access_token_expire_seconds = access_token_expire_seconds
        self._secret_key = secret_key
        self._algorithm_name = algorithm_name

    @property
    def secret_key(self) -> Union[dict, str]:
        """
        Возвращает текущий секретный ключ.

        Returns:
            Union[dict, str]: Текущий секретный ключ.
        """
        return self._secret_key

    @secret_key.setter
    def secret_key(self, secret_key: Union[dict, str]):
        """
        Устанавливает новый секретный ключ.

        Args:
            secret_key (Union[dict, str]): Новый секретный ключ.

        Raises:
            ValueError: Если переданный ключ не является строкой или словарём.
        """
        if not isinstance(secret_key, Union[dict, str]):
            raise ValueError('Секретный ключ должен быть словарем')
        self._secret_key = secret_key

    def create_token(
        self,
        user_id: uuid.UUID,
    ) -> Token:
        """
        Создает и возвращает токены доступа и обновления для пользователя.

        Args:
            user_id (int): ID пользователя, для которого создается
            токен подтверждения доступа.

        Returns:
            Token: Объект Token, содержащий токены доступа и обновления.
        """
        access_token = self._create_access_token(
            user_id=user_id,
        )
        refresh_token = self._create_refresh_token()

        return Token(
            access_token=access_token,
            refresh_token=refresh_token,
        )

    def _create_access_token(
        self,
        user_id: uuid.UUID,
    ) -> str:
        """
        Создает токен доступа для указанного пользователя.

        Args:
            user_id (int): ID пользователя, для которого создается
            токен подтверждения доступа.

        Returns:
            str: Сгенерированный токен доступа.
        """
        created_at: datetime = datetime.now(timezone.utc)
        exp = timedelta(seconds=self._access_token_expire_seconds)
        exp += created_at
        token_data: dict = {
            'sub': str(user_id),
            'iat': created_at,
            'exp': exp,
        }
        return jwt.encode(
            token_data,
            key=self._secret_key,
            algorithm=self._algorithm_name,
        )

    def _create_refresh_token(self) -> uuid.UUID:
        """
        Создает новый токен обновления.

        Returns:
            UUID: Уникальный идентификатор токена обновления.
        """
        return uuid.uuid4()
