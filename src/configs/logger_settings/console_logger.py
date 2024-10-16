import sys
from typing import Final

_LOGGER_FORMAT: Final = (
    '{time:YYYY-MM-DD HH:mm:ss.SSS}' +
    ' | <level>{level: <8}</level> |' +
    ' <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan>' +
    ' - <level>{message}</level>'
)

CONSOLE_HANDLERS: Final = (
    {
        'sink': sys.stdout,
        'format': _LOGGER_FORMAT,
        'level': 'DEBUG',
        'backtrace': False,
        'diagnose': False,
    },
)
