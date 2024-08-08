import os
from typing import Final

from dotenv import load_dotenv

load_dotenv()

POSTGRES_HOST: Final = os.environ.get('POSTGRES_HOST')
POSTGRES_PORT: Final = os.environ.get('POSTGRES_PORT')
POSTGRES_USER: Final = os.environ.get('POSTGRES_USER')
POSTGRES_PASSWORD: Final = os.environ.get('POSTGRES_PASSWORD')
POSTGRES_DB: Final = os.environ.get('POSTGRES_DB')

ASYNC_POSTGRES_URL: Final = (
    'postgresql+asyncpg://' +
    '{POSTGRES_USER}:'.format(POSTGRES_USER=POSTGRES_USER) +
    '{POSTGRES_PASSWORD}@'.format(POSTGRES_PASSWORD=POSTGRES_PASSWORD) +
    '{POSTGRES_HOST}:'.format(POSTGRES_HOST=POSTGRES_HOST) +
    '{POSTGRES_PORT}/'.format(POSTGRES_PORT=POSTGRES_PORT) +
    '{POSTGRES_DB}'.format(POSTGRES_DB=POSTGRES_DB)
)


REDIS_HOST: Final = os.environ.get('REDIS_HOST')
REDIS_PORT: Final = os.environ.get('REDIS_PORT')
