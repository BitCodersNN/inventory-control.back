# flake8: noqa: WPS300

__all__ = (
    'logger',
    'setup_uvicorn_logger',
)

from .logger_config import logger
from .uvicorn_logger import setup_uvicorn_logger
