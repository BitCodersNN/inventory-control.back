from pydantic import BaseModel


class login(BaseModel):
    login: str
    password: str
