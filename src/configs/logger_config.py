import os
import sys
from typing import Final

from loguru import logger
from loki_logger_handler.formatters.loguru_formatter import LoguruFormatter
from loki_logger_handler.loki_logger_handler import LokiLoggerHandler


def _create_filter(condition):
    return lambda record: condition(record['level'].no)


MODE: Final = os.getenv('MODE', 'Debug')

SINK: Final = sys.stdout if MODE == 'Debug' else LokiLoggerHandler(
    url='http://loki:3100/loki/api/v1/push',
    labels={'app': 'inventory-control'},
    labelKeys={},
    timeout=10,
    defaultFormatter=LoguruFormatter(),
)

LOGGER_FORMAT: Final = (
    '<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green>' +
    ' | <level>{level: <8}</level> |' +
    ' <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan>' +
    ' - <level>{message}</level>'
)

ERROR_FILTER: Final = _create_filter(
    lambda level_no: level_no >= logger.level('ERROR').no,
)
INFO_FILTER: Final = _create_filter(
    lambda level_no: level_no < logger.level('ERROR').no,
)


logger.configure(
    handlers=[
        {
            'sink': SINK,
            'format': LOGGER_FORMAT,
            'filter': INFO_FILTER,
            'level': 'DEBUG',
            'diagnose': False
        },
        {
            'sink': SINK,
            'format': LOGGER_FORMAT,
            'filter': ERROR_FILTER,
            'level': 'ERROR',
            'backtrace': False,
            'diagnose': False
        },
    ],
)
