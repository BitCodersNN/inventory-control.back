from fastapi import HTTPException, status


class TokenLimitExceededError(Exception):
    """
    Исключение, возникающее при превышении лимита токенов для пользователя.

    Attributes:
        user_id (int): Идентификатор пользователя.
        max_tokens (int): Максимально допустимое количество токенов.
        current_tokens (int): Текущее количество токенов у пользователя.
    """

    def __init__(self, user_id, max_tokens, current_tokens):
        """
        Инициализирует экземпляр исключения TokenLimitExceededError.

        Args:
            user_id (int): Идентификатор пользователя.
            max_tokens (int): Максимально допустимое количество токенов.
            current_tokens (int): Текущее количество токенов у пользователя.
        """
        self.user_id = user_id
        self.max_tokens = max_tokens
        self.current_tokens = current_tokens
        super().__init__(self.message)

    @property
    def message(self):
        """
        Возвращает сообщение об ошибке с деталями превышения лимита токенов.

        Returns:
            str: Сообщение об ошибке.
        """
        user_id = self.user_id
        max_tokens = self.max_tokens
        current_tokens = self.current_tokens
        return (
            f'Превышен лимит токенов у пользователя с id: {user_id}. '
            f'Лимит: {max_tokens}, текущее количество: {current_tokens}.'
        )


class InvalidRefreshTokenError(HTTPException):
    """
    Исключение, возникающее при использовании недопустимого токен обновления.

    Attributes:
        status_code (int): HTTP-статус код ошибки (401).
        detail (str): Детальное описание ошибки.
    """

    def __init__(self):
        """
        Инициализирует экземпляр исключения InvalidRefreshTokenError.

        Устанавливает HTTP-статус код 401 и детали ошибки.
        """
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Недопустимый токен обновления',
        )


class InvalidAccessTokenError(HTTPException):
    """
    Исключение, возникающее при использовании недопустимого токен доступа.

    Attributes:
        status_code (int): HTTP-статус код ошибки (401).
        detail (str): Детальное описание ошибки.
    """

    def __init__(self):
        """
        Инициализирует экземпляр исключения InvalidAccessTokenError.

        Устанавливает HTTP-статус код 401 и детали ошибки.
        """
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Недопустимый токен доступа',
        )


class TokenExpiredError(HTTPException):
    """
    Исключение, возникающее при попытке использовать истекший токен.

    Attributes:
        status_code (int): HTTP-статус код ошибки (401).
        detail (str): Детальное описание ошибки.
    """

    def __init__(self):
        """
        Инициализирует экземпляр исключения TokenExpiredError.

        Устанавливает HTTP-статус код 401 и детали ошибки.
        """
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Срок действия токена истек',
        )


class InvalidCredentialsError(HTTPException):
    """
    Исключение, возникающее при предоставлении неверных учетных данных.

    Attributes:
        status_code (int): HTTP-статус код ошибки (400).
        detail (str): Детальное описание ошибки.
    """

    def __init__(self):
        """
        Инициализирует экземпляр исключения InvalidCredentialsError.

        Устанавливает HTTP-статус код 400 и детали ошибки.
        """
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Неправильный логин или пароль',
        )


class RefreshNotExistError(HTTPException):
    """
    Исключение, рефрешь токен не существует.

    Attributes:
        status_code (int): HTTP-статус код ошибки (404).
        detail (str): Детальное описание ошибки.
    """

    def __init__(self):
        """
        Инициализирует экземпляр исключения RefreshNotExistError.

        Устанавливает HTTP-статус код 404 и детали ошибки.
        """
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Рефрешь токен не найден',
        )


class UnexpectedError(HTTPException):
    """
    Исключение, возникающее при возникновении неожиданной ошибки на сервере.

    Attributes:
        status_code (int): HTTP-статус код ошибки (500).
        detail (str): Детальное описание ошибки.
    """

    def __init__(self):
        """
        Инициализирует экземпляр исключения UnexpectedError.

        Устанавливает HTTP-статус код 500 и детали ошибки.
        """
        super().__init__(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail='хз че там',
        )
