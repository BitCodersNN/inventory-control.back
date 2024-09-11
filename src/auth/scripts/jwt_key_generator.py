import os
from typing import Final

import yaml
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa

from src.configs.logger.logger_config import logger

TOKEN_ALGORITHM_TYPE: Final = os.environ.get('TOKEN_ALGORITHM_TYPE', 'symmetric')


def _generate_jwt_keys() -> dict[str, bytes]:
    match TOKEN_ALGORITHM_TYPE:
        case 'symmetric':
            return _generate_jwt_key_for_symmetric_algorithm()
        case 'asymmetric':
            return _generate_jwt_keys_for_asymmetric_algorithm()
        case _:
            raise TypeError('Неподдерживаемый тип алгоритма')


def _save_secret_to_file(filename='src/auth/configs/jwt_key.yaml', **kwargs):
    with open(filename, 'w') as file:
        yaml.dump(kwargs, file, default_flow_style=False)


def _generate_jwt_key_for_symmetric_algorithm(length: int = 32) -> dict[str, bytes]:
    return {'secret_key': os.urandom(length)}


def _generate_jwt_keys_for_asymmetric_algorithm() -> dict[str, bytes]:
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
        backend=default_backend()
    )

    private_pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption()
    )

    public_key = private_key.public_key()

    public_pem = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )

    return {
        'secret_key': private_pem,
        'public_key': public_pem,
    }


def main():
    try:
        _save_secret_to_file(**_generate_jwt_keys())
    except Exception as ex:
        logger.critical(
            f'You have done something wrong! {str(ex)}',
            labels={
                'script': 'jwt_key_generator',
            },
        )


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        logger.critical('Shutting down, bye!')
