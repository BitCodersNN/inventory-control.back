from fastapi import APIRouter, Response
from starlette.status import HTTP_200_OK  # noqa: F401

from src.auth import schemas  # noqa: F401
from src.auth.models import users  # noqa: F401

router = APIRouter()


@router.get('/echo/{string}')
def set_task(string: str, response: Response) -> str:
    """Example."""
    return string[::-1]
