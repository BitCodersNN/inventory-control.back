from datetime import datetime, timedelta, timezone
from uuid import UUID, uuid4

from jose import jwt


class TokenFactory:
    """
    Класс для создания токенов доступа и обновления.

    Attributes:
        _access_token_expire_seconds (int): Время жизни токена доступа в сек.
        _secret_key (str): Секретный ключ, используемый для подписи токенов.
        _algorithm_name (str): Название алгоритма, подписывающего токены.

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
        secret_key: str,
        algorithm_name: str,
    ):
        """
        Инициализация класса TokenFactory.

        Args:
            access_token_expire_seconds (int): Время жизни токена доступа в сек.
            secret_key (str): Секретный ключ, используемый для подписи токенов.
            algorithm_name (str): Название алгоритма, подписывающего токены.
        """
        self._access_token_expire_seconds = access_token_expire_seconds
        self._secret_key = secret_key
        self._algorithm_name = algorithm_name

    @property
    def secret_key(self) -> str:
        """
        Возвращает текущий секретный ключ.

        Returns:
            str: Текущий секретный ключ.
        """
        return self.secret_key

    @secret_key.setter
    def secret_key(self, secret_key: str):
        """
        Устанавливает новый секретный ключ.

        Args:
            secret_key (str): Новый секретный ключ. Должен быть строкой.

        Raises:
            ValueError: Если переданный ключ не является строкой.
        """
        if not isinstance(secret_key, str):
            raise ValueError('Секретный ключ должен быть строкой')
        self.secret_key = secret_key

    def create_access_token(
        self,
        user_id,
    ) -> str:
        """
        Создает токен доступа для указанного пользователя.

        Аргументы:
            user_id: ID пользователя, для которого создается токен доступа.

        Возвращает:
            str: Сгенерированный токен доступа.
        """
        created_at: datetime = datetime.now(timezone.utc)
        exp = timedelta(seconds=self._access_token_expire_seconds)
        exp += created_at
        token_data: dict = {
            'sub': user_id,
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

        Возвращает:
            UUID: Уникальный идентификатор токена обновления.
        """
        return uuid4()
