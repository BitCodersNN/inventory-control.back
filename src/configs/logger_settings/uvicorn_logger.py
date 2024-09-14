import re

import uvicorn

from src.configs.logger_settings.logger_config import logger


def _determine_log_level(message):
    match = re.search('CRITICAL|ERROR|WARNING|INFO', message, re.IGNORECASE)
    return match.group(0).upper() if match else 'DEBUG'


class _InterceptHandler:
    """
    Обработчик для перехвата и логирования сообщений с определенным уровнем.

    Methods:
        write(message: str) -> None: Обрабатывает и логирует сообщение.
    """

    def write(self, message):
        """
        Обрабатывает и логирует сообщение с определенным уровнем.

        Args:
            message (str): Сообщение для логирования.
        """
        level = _determine_log_level(message)
        cleaned_message = re.sub(r'^\w+:\s*', '', message)
        logger.opt(depth=6).log(
            level,
            cleaned_message.strip(),
            labels={'logger_name': 'uvicorn'},
        )


def setup_uvicorn_logger():
    """
    Настройка логгера uvicorn с заменой обработчиков на `InterceptHandler`.

    Returns:
        dict: Конфигурация логирования uvicorn.
    """
    uvicorn_logger = uvicorn.config.LOGGING_CONFIG
    uvicorn_logger['handlers']['default']['stream'] = _InterceptHandler()
    uvicorn_logger['handlers']['access']['stream'] = _InterceptHandler()
    return uvicorn_logger
