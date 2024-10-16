from src.auth.configs.token_config import (
    TOKEN_ALGORITHM_NAME,
    TOKEN_ALGORITHM_TYPE,
    YAML_FILE_PATH,
)
from src.configs.logger_settings import logger

from .jwt_generators.jwt_key_generator import IJWTKeyGenerator
from .jwt_generators.key_generator_factory import create_generator
from .jwt_key_storage import save_jwt_keys_to_file


def _generate_and_save_keys():
    generator: IJWTKeyGenerator = create_generator(
        TOKEN_ALGORITHM_TYPE,
        TOKEN_ALGORITHM_NAME,
    )
    keys: dict[str, bytes] = generator.generate_keys()
    save_jwt_keys_to_file(YAML_FILE_PATH, **keys)


def _main():
    try:
        _generate_and_save_keys()
    except Exception as ex:
        logger.critical(
            'You have done something wrong! {0}'.format(str(ex)),
            labels={
                'script': 'jwt_key_generator',
            },
        )


if __name__ == '__main__':
    try:
        _main()
    except KeyboardInterrupt:
        logger.critical('Shutting down, bye!')
