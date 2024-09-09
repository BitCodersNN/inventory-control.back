from fastapi import HTTPException, status


class TokenLimitExceededError(Exception):
    def __init__(self, user_id, max_tokens, current_tokens):
        self.user_id = user_id
        self.max_tokens = max_tokens
        self.current_tokens = current_tokens
        super().__init__(self.message)

    @property
    def message(self):
        return (
            f'Превышен лимит токенов у пользователя с id: {self.user_id}. '
            f'Лимит: {self.max_tokens}, текущее количество: {self.current_tokens}.'
        )


class InvalidRefreshTokenError(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Недопустимый токен обновления',
        )


class InvalidAccessTokenError(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Недопустимый токен доступа',
        )


class TokenExpiredError(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Срок действия токена истек',
        )
