import uvicorn
from loguru import logger

from src.config import SERVER_PORT


def main():
    """Main method. Entry point."""
    try:
        uvicorn.run('src.api:app', port=SERVER_PORT, reload=True)
    except Exception as ex:
        logger.critical('You have done something wrong! {0}'.format(str(ex)))


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        logger.critical('Shutting down, bye!')
