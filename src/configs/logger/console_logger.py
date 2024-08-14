import sys
from typing import Final

from loguru import logger


def _create_filter(condition):
    return lambda record: condition(record['level'].no)


_LOGGER_FORMAT: Final = (
    '<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green>' +
    ' | <level>{level: <8}</level> |' +
    ' <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan>' +
    ' - <level>{message}</level>'
)

_ERROR_FILTER: Final = _create_filter(
    lambda level_no: level_no >= logger.level('ERROR').no,
)
_INFO_FILTER: Final = _create_filter(
    lambda level_no: level_no < logger.level('ERROR').no,
)

CONSOLE_HANDLERS: Final = (
    {
        'sink': sys.stdout,
        'format': _LOGGER_FORMAT,
        'filter': _INFO_FILTER,
        'level': 'DEBUG',
        'diagnose': False,
    },
    {
        'sink': sys.stdout,
        'format': _LOGGER_FORMAT,
        'filter': _ERROR_FILTER,
        'level': 'ERROR',
        'backtrace': False,
        'diagnose': False,
    },
)
