from src.configs.logger.logger_config import logger


def main():
    """Main method. Entry point."""
    try:
        a = 10/0
        ...  # noqa: WPS428
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
