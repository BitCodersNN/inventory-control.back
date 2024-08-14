from src.configs.logger.logger_config import logger
import uvicorn
from loguru import logger

from src.config import SERVER_PORT


def main():
    """Main method. Entry point."""
    try:
        uvicorn.run('src.api:app', port=SERVER_PORT, reload=True)
    except Exception as ex:
        logger.opt(exception=True).critical(
            'You have done something wrong! {0}'.format(str(ex)),
            labels={'service_name': 'auth'},
        )


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        logger.opt(exception=True).critical('Shutting down, bye!')
