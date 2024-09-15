from types import MappingProxyType
from typing import Final

MAX_TOKEN_COUNT: Final = 5

LABELS_FOR_LOGGER: Final = MappingProxyType(
    {
        'service': 'auth',
    },
)
