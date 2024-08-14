import os
from typing import Final

from loguru import logger

from src.configs.logger.console_logger import CONSOLE_HANDLERS
from src.configs.logger.loki_logger import LOKI_LOGGER_HANDLER


def _get_handlers(mode):
    match mode:
        case 'Debug':
            return CONSOLE_HANDLERS
        case 'Release':
            return LOKI_LOGGER_HANDLER


_MODE: Final = os.getenv('MODE', 'Debug')


logger.configure(
    handlers=_get_handlers(_MODE),
)
