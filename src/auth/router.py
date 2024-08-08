from fastapi import APIRouter, Response
from starlette.status import *
from . import schemas
from .models import *

router = APIRouter()


@router.get("/echo/{string}")
def set_task(string: str, response: Response) -> str:
    response = HTTP_200_OK
    return string[::-1]
