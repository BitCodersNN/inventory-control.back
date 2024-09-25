from typing import Union

from src.auth.models import RefreshSessionModel
from src.auth.schemas.access_token_payload import AccessTokenPayload
from src.auth.schemas.tokens import AccessTokenConfig, Tokens
from src.auth.utils.tokens.access_token_decoder import AccessTokenDecoder
from src.auth.utils.tokens.refresh_session_validator import (
    RefreshSessionValidator,
)
from src.auth.utils.tokens.token_factory import TokenFactory


class TokenToolkit:  # noqa: WPS214
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
        token_config: AccessTokenConfig,
    ):
        """
        Инициализация класса TokenFacade.

        Args:
            token_config (AccessTokenConfig): Конфигурация токенов доступа.
            payload_handler (Type[PayloadHandler]): Обработчик полезной
            нагрузки токена.
        """
        self._token_factory = TokenFactory(
            token_config.access_token_expire_seconds,
            token_config.secret_key,
            token_config.algorithm_name,
        )
        self._refresh_session_validator = RefreshSessionValidator()
        self._access_token_decoder = AccessTokenDecoder(
            token_config.verification_key or token_config.secret_key,
            token_config.algorithm_name,
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

    def create_token(self, payload: AccessTokenPayload) -> Tokens:
        """
        Создает токены доступа и обновления для указанного пользователя.

        Args:
            payload (AccessTokenPayload): Полезная нагрузка JWT.

        Returns:
            Tokens: Объект, содержащий токены доступа и обновления.
        """
        payload: dict = payload.dict()
        return self._token_factory.create_token(**payload)

    def refresh(
        self,
        refresh_session: RefreshSessionModel,
        payload: AccessTokenPayload,
    ) -> Tokens:
        """
        Обновляет токены доступа и обновления.

        Args:
            refresh_session (RefreshSessionModel): Объект обновления сессии.
            payload (AccessTokenPayload): Полезная нагрузка JWT.

        Returns:
            Tokens: Объект, содержащий новые токены доступа и обновления.
        """
        self._refresh_session_validator.verify_refresh_session(
            refresh_session,
            payload.sub,
        )
        return self.create_token(payload)

    def decode_token(self, access_token: str) -> AccessTokenPayload:
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
        payload: dict = self._access_token_decoder.decode_token(access_token)
        return AccessTokenPayload.parse_obj(payload)
