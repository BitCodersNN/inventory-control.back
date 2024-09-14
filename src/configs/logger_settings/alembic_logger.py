import logging

from src.configs.logger_settings.logger_config import logger


class _LoguruHandler(logging.Handler):
    def emit(self, record):
        log_entry = self.format(record)
        logger.opt(depth=6).log(
            record.levelname,
            log_entry,
            labels={'logger_name': 'alembic'},
        )


def setup_alembic_logger():
    """
    Настраивает Alembic для логирования через Loguru.

    Предотвращает дублирование записей и централизует управление логами.
    """
    alembic_logger = logging.getLogger('alembic')
    alembic_logger.handlers = [_LoguruHandler()]
    alembic_logger.propagate = False
