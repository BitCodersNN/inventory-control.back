from typing import Union

from jose import jwt

from src.auth.utils.constants import LABELS_FOR_LOGGER
from src.auth.utils.exceptions import (
    InvalidAccessTokenError,
    TokenExpiredError,
)
from src.configs.logger_settings import logger


class AccessTokenDecoder:
    """
    Класс для декодирования JWT-токенов доступа.

    Methods:
        verification_key (property): Возвращает текущий ключ проверки.
        verification_key (setter): Устанавливает новый ключ проверки.
        decode_token: Декодирует токен доступа и возвращает
        его полезную нагрузку.
    """

    def __init__(
        self,
        verification_key: Union[dict, str],
        algorithm_name: str,
    ):
        """
        Инициализация объекта AccessTokenDecoder.

        Args:
            verification_key (Union[dict, str]): Ключ для проверки
            подлинности токена.
            algorithm_name (str): Название алгоритма, подписывающего токены.
        """
        self._verification_key = verification_key
        self._algorithm_name = algorithm_name

    @property
    def verification_key(self) -> Union[dict, str]:
        """
        Возвращает текущий ключ проверки.

        Returns:
            Union[dict, str]: Текущий ключ проверки.
        """
        return self._verification_key

    @verification_key.setter
    def verification_key(self, verification_key: Union[dict, str]):
        """
        Устанавливает новый ключ проверки.

        Args:
            verification_key (Union[dict, str]): Новый ключ проверки.

        Raises:
            ValueError: Если переданный ключ не является строкой или словарём.
        """
        if not isinstance(verification_key, Union[dict, str]):
            raise ValueError('Ключ проверки должен словарем')
        self._verification_key = verification_key

    def decode_token(
        self,
        access_token: str,
    ) -> dict:
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
        try:
            decoded_payload = jwt.decode(
                access_token,
                self._verification_key,
                algorithms=self._algorithm_name,
            )
        except jwt.ExpiredSignatureError:
            logger.info(
                (
                    'Cрок действия токена доступа истек.'
                    f'access_token = {access_token}'
                ),
                labels=LABELS_FOR_LOGGER,
            )
            raise TokenExpiredError
        except jwt.JWTError:
            logger.info(
                (
                    'Неверный токен доступа.'
                    f'access_token = {access_token}'
                ),
                labels=LABELS_FOR_LOGGER,
            )
            raise InvalidAccessTokenError

        decoded_payload['sub'] = UUID(decoded_payload['sub'])
        return decoded_payload
