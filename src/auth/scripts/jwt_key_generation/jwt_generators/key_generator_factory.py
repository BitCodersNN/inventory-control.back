from types import MappingProxyType
from typing import Final, Optional

from .jwt_key_generator import IJWTKeyGenerator
from .rsa_jwt_key_generator import RsaJWTKeyGenerator
from .symmetric_jwt_key_generator import SymmetricJWTKeyGenerator

ALGORITHM_MAP: Final = MappingProxyType(
    {
        'symmetric': SymmetricJWTKeyGenerator,
        'asymmetric': {
            'RS256': RsaJWTKeyGenerator,
        },
    },
)


def create_generator(
    algorithm_type: str,
    algorithm_name: Optional[str] = None,
) -> IJWTKeyGenerator:
    """
    Создает генератор ключей JWT на основе указанного типа и имени алгоритма.

    Args:
        algorithm_type (str): Тип алгоритма
            (например, 'symmetric' или 'asymmetric').
        algorithm_name (Optional[str]): Имя алгоритма
            (например, 'RS256').
            По умолчанию: None.

    Returns:
        IJWTKeyGenerator: Экземпляр генератора ключей JWT.

    Raises:
        TypeError: Если указан неподдерживаемый тип алгоритма или имя алгоритма.
    """
    generator_class = ALGORITHM_MAP.get(algorithm_type)

    if generator_class is None:
        raise TypeError(f'Неподдерживаемый тип алгоритма: {algorithm_type}')

    if isinstance(generator_class, dict):
        generator_class = generator_class.get(algorithm_name)
        if generator_class is None:
            raise TypeError(f'Неподдерживаемый алгоритм: {algorithm_name}')

    return generator_class()
