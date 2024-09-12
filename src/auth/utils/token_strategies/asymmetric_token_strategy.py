from jose import jwt

from src.auth.utils.token_strategies.token_strategy import TokenStrategy


class AsymmetricTokenStrategy(TokenStrategy):
    """
    Класс для создания и декодирования токенов доступа и обновления.

    Использует асимметричный алгоритм.

    Наследуется от абстрактного класса TokenStrategy.
    """

    def __init__(
        self,
        access_token_expire_seconds: int,
        secret_key: str,
        public_key: str,
        algorithm_name: str,
    ):
        """
        Инициализация класса AsymmetricTokenStrategy.

        Args:
            access_token_expire_seconds (int): Время жизни токена доступа
            в секундах.
            secret_key (str): Секретный ключ, используемый для подписи токенов.
            public_key (str): Публичный ключ, используемый для проверки
            подписи токенов.
            algorithm_name (str): Название алгоритма, используемого
            для подписи токенов.
        """
        super().__init__(
            access_token_expire_seconds,
            secret_key,
            algorithm_name,
        )
        self._public_key = public_key

    def decode_token(self, access_token: str) -> dict:
        """
        Декодирует токен доступа с использованием асимметричного алгоритма.

        Args:
            access_token (str): Токен доступа, который нужно декодировать.

        Returns:
            dict: Декодированные данные токена.

        Raises:
            JWTError: Если подпись каким-либо образом недействительна.
            ExpiredSignatureError: Если срок действия подписи истек.
            JWTClaimsError: Если какое-либо утверждение недействительно
            каким-либо образом.
        """
        return jwt.decode(
            access_token,
            self._public_key,
            algorithms=[self._algorithm_name],
        )
