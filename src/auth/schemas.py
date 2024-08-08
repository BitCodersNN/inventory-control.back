from pydantic import BaseModel


class Login(BaseModel):
    """Передается при входе."""

    login: str
    password: str
