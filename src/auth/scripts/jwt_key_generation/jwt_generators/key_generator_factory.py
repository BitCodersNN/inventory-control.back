import os
from typing import Final

from .asymmetric_jwt_key_generator import AsymmetricJWTKeyGenerator
from .jwt_key_generator import IJWTKeyGenerator
from .symmetric_jwt_key_generator import SymmetricJWTKeyGenerator

TOKEN_ALGORITHM_TYPE: Final = os.environ.get(
    'TOKEN_ALGORITHM_TYPE',
    default='asymmetric',
)


def create_generator() -> IJWTKeyGenerator:
    """
    Создает и возвращает генератор ключей JWT в зависимости от типа алгоритма.

    Returns:
        IJWTKeyGenerator: Экземпляр генератора ключей JWT.

    Raises:
        TypeError: Если указан неподдерживаемый тип алгоритма.
    """
    match TOKEN_ALGORITHM_TYPE:
        case 'symmetric':
            return SymmetricJWTKeyGenerator()
        case 'asymmetric':
            return AsymmetricJWTKeyGenerator()
        case _:
            raise TypeError('Неподдерживаемый тип алгоритма')
