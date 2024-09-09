import uvicorn

from src.configs.logger_settings import logger, setup_uvicorn_logger
from src.configs.server_config import SERVER_HOST, SERVER_PORT


def main():
    """Main method. Entry point."""
    try:
        uvicorn.run(
            'src.api:app',
            host=SERVER_HOST,
            port=SERVER_PORT,
            reload=True,
            log_config=setup_uvicorn_logger(),
        )
    except Exception as ex:
        logger.opt(exception=True).critical(
            'You have done something wrong! {0}'.format(str(ex)),
        )


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        logger.opt(exception=True).critical('Shutting down, bye!')
