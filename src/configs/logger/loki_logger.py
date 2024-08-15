import os
import traceback
from typing import Final

from loki_logger_handler.loki_logger_handler import LokiLoggerHandler

_LOKI_URL: Final = os.getenv('LOKI_URL')
_APP_LABEL: Final = 'inventory-control'
_MESSAGE_KEY: Final = 'message'
_TIMESTAMP_KEY: Final = 'timestamp'
_LEVEL_KEY: Final = 'level'
_FILE_KEY: Final = 'file'
_PATH_KEY: Final = 'path'
_LINE_KEY: Final = 'line'
_STACKTRACE_KEY: Final = 'stacktrace'
_FUNCTION_KEY: Final = 'function'
_NAME_KEY: Final = 'name'
_EXTRA_KEY: Final = 'extra'
_LABELS_KEY: Final = 'labels'
_TIME_KEY: Final = 'time'
_EXCEPTION_KEY: Final = 'exception'
_STACKTRACE_ENABLED_LEVELS: Final = ('ERROR', 'CRITICAL')


class _CustomLokiLoggerHandler(LokiLoggerHandler):
    """
    Кастомный обработчик логов для Loki, расширяющий базовый LokiLoggerHandler.

    Переопределяет метод `emit` для настройки меток в сообщениях логов.
    Объединяет предопределенные метки с метками из записи лога
    и дополнительными метками.
    """

    def emit(self, record):
        labels_from_record = {
            _FUNCTION_KEY: record.get(_FUNCTION_KEY),
            _NAME_KEY: record.get(_NAME_KEY),
        }
        additional_labels = record.get(_EXTRA_KEY).pop(_LABELS_KEY, {})

        all_labels = {
            **self.labels,
            **additional_labels,
            **labels_from_record,
        }

        custom_handler = LokiLoggerHandler(
            url=self.request.url,
            labels=all_labels,
            labelKeys=self.labelKeys,
            timeout=self.timeout,
            defaultFormatter=self.logger_formatter,
        )

        custom_handler.emit(record)


class _CustomLoguruFormatter:
    """
    Кастомный форматтер для логов Loguru.

    Предоставляет метод форматирования записей логов, включая сообщение,
    временную метку и уровень логирования.
    Опционально включает дополнительную информацию, такую как имя файла,
    путь, номер строки и трассировку стека для определенных уровней логирования.
    """

    def format(self, record):
        formatted = {
            _MESSAGE_KEY: record.get(_MESSAGE_KEY),
            _TIMESTAMP_KEY: record.get(_TIME_KEY).timestamp(),
            _LEVEL_KEY: record.get(_LEVEL_KEY).name,
        }

        if record.get(_EXTRA_KEY):
            if record.get(_EXTRA_KEY).get(_EXTRA_KEY):
                formatted.update(record.get(_EXTRA_KEY).get(_EXTRA_KEY))
            else:
                formatted.update(record.get(_EXTRA_KEY))

        if record.get(_LEVEL_KEY).name in _STACKTRACE_ENABLED_LEVELS:
            formatted[_FILE_KEY] = record.get(_FILE_KEY).name
            formatted[_PATH_KEY] = record.get(_FILE_KEY).path
            formatted[_LINE_KEY] = record.get(_LINE_KEY)

            if record.get(_EXCEPTION_KEY):
                exc_type, exc_value, exc_traceback = record.get(_EXCEPTION_KEY)
                formatted_traceback = traceback.format_exception(
                    exc_type,
                    exc_value,
                    exc_traceback,
                )
                formatted[_STACKTRACE_KEY] = ''.join(formatted_traceback)

        return formatted


LOKI_LOGGER_HANDLER: Final = (
    {
        'sink': _CustomLokiLoggerHandler(
            url=_LOKI_URL,
            labels={'app': _APP_LABEL},
            labelKeys={},
            timeout=10,
            defaultFormatter=_CustomLoguruFormatter(),
        ),
    },
)
