import base64
from typing import Final, Optional

import yaml

_YAML_FILE_PATH: Final = 'src/auth/configs/jwt_key.yaml'


with open(_YAML_FILE_PATH, 'r') as file:  # noqa: WPS110
    keys = yaml.safe_load(file)

_PUBLIC_KEY_VALUE: Final = keys.get('public_key')
_SECRET_KEY_VALUE: Final = keys.get('secret_key')

PUBLIC_KEY: Final[Optional[str]] = (
    base64.b64encode(_PUBLIC_KEY_VALUE).decode('utf-8')
    if _PUBLIC_KEY_VALUE is not None else None
)

SECRET_KEY: Final[Optional[str]] = (
    base64.b64encode(_SECRET_KEY_VALUE).decode('utf-8')
    if _SECRET_KEY_VALUE is not None else None
)
