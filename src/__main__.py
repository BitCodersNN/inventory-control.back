from src.configs.logger_config import logger


def main():
    """Main method. Entry point."""
    try:
        ...  # noqa: WPS428
    except Exception as ex:
        logger.opt(exception=True).critical(
            'You have done something wrong! {0}'.format(str(ex)),
        )


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        logger.opt(exception=True).critical('Shutting down, bye!')
