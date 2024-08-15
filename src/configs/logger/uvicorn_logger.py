import re

import uvicorn

from src.configs.logger.logger_config import logger


class _InterceptHandler:
    """
    Обработчик для перехвата и логирования сообщений с определенным уровнем.

    Methods:
        write(message: str) -> None:
            Обрабатывает и логирует сообщение.
    """

    def write(self, message):
        """
        Обрабатывает и логирует сообщение с определенным уровнем.

        Args:
            message (str): Сообщение для логирования.
        """
        level = self._determine_log_level(message)
        cleaned_message = re.sub(r'^\w+:\s*', '', message)
        logger.opt(depth=1).log(level, cleaned_message.strip())

    def _determine_log_level(self, message):
        match = re.search('CRITICAL|ERROR|WARNING|INFO', message, re.IGNORECASE)
        return match.group(0).upper() if match else 'DEBUG'


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
