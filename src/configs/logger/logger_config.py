import os
from typing import Final

from loguru import logger

from src.configs.logger.console_logger import CONSOLE_HANDLERS
from src.configs.logger.loki_logger import LOKI_LOGGER_HANDLER

handlers: Final = {
    'Debug': CONSOLE_HANDLERS,
    'Release': CONSOLE_HANDLERS + LOKI_LOGGER_HANDLER,
}

_MODE: Final = os.getenv('MODE', 'Debug')

logger.configure(
    handlers=handlers.get(_MODE, CONSOLE_HANDLERS),
)
