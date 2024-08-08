from loguru import logger
import uvicorn


def main():
    """Main method. Entry point."""
    try:
        uvicorn.run('api:app', port=8000, reload=True)
    except Exception as ex:
        logger.critical('You have done something wrong! {0}'.format(str(ex)))


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        logger.critical('Shutting down, bye!')
