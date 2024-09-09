import os
from typing import Final

from loguru import logger

from src.configs.logger_settings.console_logger import CONSOLE_HANDLERS
from src.configs.logger_settings.loki_logger import LOKI_LOGGER_HANDLER


def _error_with_exception(message, *args, **kwargs):
    logger.opt(exception=True).error(message, *args, **kwargs)


def _critical_with_exception(message, *args, **kwargs):
    logger.opt(exception=True).critical(message, *args, **kwargs)


_handlers: Final = {
    'Debug': CONSOLE_HANDLERS,
    'Release': CONSOLE_HANDLERS + LOKI_LOGGER_HANDLER,
}

_MODE: Final = os.getenv('MODE', 'Debug')

logger.configure(
    handlers=_handlers.get(_MODE, CONSOLE_HANDLERS),
)

logger.error = _error_with_exception
logger.critical = _critical_with_exception
