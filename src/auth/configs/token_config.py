import os
from typing import Final, Optional

import yaml
from dotenv import load_dotenv

load_dotenv()

YAML_FILE_PATH: Final = os.environ.get(
    'FILE_WITH_JWT_KEY',
    default='src/auth/configs/jwt_key.yaml',
)

try:
    with open(YAML_FILE_PATH, 'r') as file:  # noqa: WPS110
        _keys = yaml.safe_load(file)
except FileNotFoundError:
    _keys = {}

_ACCESS_TOKEN_EXPIRE_MINUTES: Final = 5
_REFRESH_TOKEN_EXPIRE_DAYS: Final = 30


PUBLIC_KEY: Final[Optional[bytes]] = _keys.get('public_key')
SECRET_KEY: Final[Optional[bytes]] = _keys.get('secret_key')

MAX_TOKEN_COUNT: Final = os.environ.get(
    'MAX_TOKEN_COUNT',
    default=5,
)

TOKEN_ALGORITHM_TYPE: Final = os.environ.get(
    'TOKEN_ALGORITHM_TYPE',
    default='asymmetric',
)
TOKEN_ALGORITHM_NAME: Final = os.environ.get(
    'TOKEN_ALGORITHM_NAME',
    default='RS256',
)

ACCESS_TOKEN_EXPIRE_SECONDS: Final = int(
    os.environ.get(
        'ACCESS_TOKEN_EXPIRE_MINUTES',
        default=_ACCESS_TOKEN_EXPIRE_MINUTES,
    ),
) * 60

REFRESH_TOKEN_EXPIRE_SECONDS: Final = int(
    os.environ.get(
        'REFRESH_TOKEN_EXPIRE_DAYS',
        default=_REFRESH_TOKEN_EXPIRE_DAYS,
    ),
) * 24 * 60
