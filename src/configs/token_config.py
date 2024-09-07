import os
from typing import Final

from dotenv import load_dotenv

load_dotenv()

SECRET_KEY: Final = os.environ.get('SECRET_KEY')
TOKEN_ALG: Final = os.environ.get('TOKEN_ALG')
ACCESS_TOKEN_EXPIRE_SECONDS: Final = (
    int(os.environ.get('ACCESS_TOKEN_EXPIRE_MINUTES')) * 60
)
REFRESH_TOKEN_EXPIRE_SECONDS: Final = (
    int(os.environ.get('REFRESH_TOKEN_EXPIRE_DAYS')) * 24 * 60
)
