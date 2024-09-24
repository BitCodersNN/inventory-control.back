import uuid
from typing import Optional, Union

from src.auth.models import RefreshSessionModel
from src.auth.schemas.token import Token
from src.auth.utils.tokens.access_token_decoder import AccessTokenDecoder
from src.auth.utils.tokens.refresh_session_validator import (
    RefreshSessionValidator,
)
from src.auth.utils.tokens.token_factory import TokenFactory


class TokenManager:  # noqa: WPS214
    """
    Управление токенами доступа и обновления.

    Attributes:
        _token_factory (TokenFactory): Фабрика для создания токенов.
        _refresh_session_validator (RefreshSessionValidator): Валидатор сессий
        обновления токенов.
        _access_token_decoder (AccessTokenDecoder): Декодер токенов доступа.

    Methods:
        secret_key (property): Возвращает текущий секретный ключ.
        secret_key (setter): Устанавливает новый секретный ключ.
        verification_key (property): Возвращает текущий ключ проверки.
        verification_key (setter): Устанавливает новый ключ проверки.
        create_tokens: Создает токены доступа и обновления
        для указанного пользователя.
        refresh: Обновляет токены доступа и обновления.
        decode_token: Декодирует токен доступа и возвращает
        его полезную нагрузку.
    """

    def __init__(
        self,
        access_token_expire_seconds: int,
        algorithm_name: str,
        secret_key: Union[dict, str],
        verification_key: Optional[Union[dict, str]],
    ):
        """
        Инициализация класса TokenFacade.

        Args:
            access_token_expire_seconds (int): Время жизни токена доступа в сек.
            algorithm_name (str): Название алгоритма, подписывающего токены.
            secret_key (Union[dict, str]): Секретный ключ, используемый
            для подписи токенов.
            verification_key (Optional[bytes]): Ключ для проверки подписи
            токенов. Если не указан, используется secret_key.
        """
        verification_key = verification_key if (
            verification_key is not None
        ) else secret_key

        self._token_factory = TokenFactory(
            access_token_expire_seconds,
            secret_key,
            algorithm_name,
        )
        self._refresh_session_validator = RefreshSessionValidator()
        self._access_token_decoder = AccessTokenDecoder(
            verification_key,
            algorithm_name,
        )

    @property
    def secret_key(self) -> Union[dict, str]:
        """
        Возвращает текущий секретный ключ.

        Returns:
            Union[dict, str]: Текущий секретный ключ.
        """
        return self._token_factory.secret_key

    @secret_key.setter
    def secret_key(self, secret_key: Union[dict, str]):
        """
        Устанавливает новый секретный ключ.

        Args:
            secret_key (Union[dict, str]): Новый секретный ключ.

        Raises:
            ValueError: Если переданный ключ не является строкой или словарём.
        """
        if not isinstance(secret_key, (str, dict)):
            raise ValueError('Секретный ключ должен быть строкой или словарём')
        self._token_factory.secret_key = secret_key

    @property
    def verification_key(self) -> Union[dict, str]:
        """
        Возвращает текущий ключ проверки.

        Returns:
            Union[dict, str]: Текущий ключ проверки.
        """
        return self._access_token_decoder.verification_key

    @verification_key.setter
    def verification_key(self, verification_key: Union[dict, str]):
        """
        Устанавливает новый ключ проверки.

        Args:
            verification_key (Union[dict, str]): Новый ключ проверки.

        Raises:
            ValueError: Если переданный ключ не является строкой или словарём.
        """
        if not isinstance(verification_key, (str, dict)):
            raise ValueError('Ключ проверки должен быть строкой или словарём')
        self._access_token_decoder.verification_key = verification_key

    def create_token(self, user_id: uuid.UUID) -> Token:
        """
        Создает токены доступа и обновления для указанного пользователя.

        Args:
            user_id (uuid.UUID): ID пользователя, для которого создаются токены.

        Returns:
            Token: Объект, содержащий токены доступа и обновления.
        """
        return self._token_factory.create_token(user_id)

    def refresh(
        self,
        refresh_session: RefreshSessionModel,
        user_id: uuid.UUID,
    ) -> Token:
        """
        Обновляет токены доступа и обновления.

        Args:
            refresh_session (RefreshSessionModel): Объект обновления сессии.
            user_id (uuid.UUID): ID пользователя, для которого обновляются
            токены.

        Returns:
            Token: Объект, содержащий новые токены доступа и обновления.
        """
        self._refresh_session_validator.verify_refresh_session(
            refresh_session,
            user_id,
        )
        return self.create_token(user_id)

    def decode_token(self, access_token: str) -> dict:
        """
        Декодирует токен доступа и возвращает его полезную нагрузку.

        Args:
            access_token (str): Токен доступа для декодирования.

        Returns:
            dict: Полезная нагрузка токена в виде словаря.

        Raises:
            TokenExpiredError: Если срок действия токена истек.
            InvalidAccessTokenError: Если токен недействителен.
        """
        return self._access_token_decoder.decode_token(access_token)
