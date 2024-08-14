from pydantic import BaseModel


class AuthorizationData(BaseModel):
    """Авторизационные данные."""

    login: str
    password: str
