import enum
from typing import Optional

from src.auth.utils.token_strategies.asymmetric_token_strategy import (
    AsymmetricTokenStrategy,
)
from src.auth.utils.token_strategies.symmetric_token_strategy import (
    SymmetricTokenStrategy,
)
from src.auth.utils.token_strategies.token_strategy import TokenStrategy


class StrategyType(enum.Enum):
    """
    Перечисление типов стратегий для создания токенов.

    Values:
        symmetric (str): Симметричный алгоритм.
        asymmetric (str): Асимметричный алгоритм.
    """

    symmetric = 'симметричный алгоритм'
    asymmetric = 'асимметричный алгоритм'


def create_strategy(
    strategy_type: StrategyType,
    access_token_expire_seconds: int,
    secret_key: str,
    algorithm_name: str,
    public_key: Optional[str] = None,
) -> TokenStrategy:
    """
    Создает и возвращает экземпляр StrategyType.

    Args:
        strategy_type (StrategyType): Тип стратегии
        (симметричная или асимметричная).
        access_token_expire_seconds (int): Время жизни токена доступа
        в секундах.
        secret_key (str): Секретный ключ, используемый для подписи токенов.
        algorithm_name (str): Название алгоритма, используемого
        для подписи токенов.
        public_key (Optional[str]): Публичный ключ, используемый
        для проверки подписи токенов (только для асимметричных стратегий).

    Returns:
        TokenStrategy: Экземпляр стратегии для создания и декодирования токенов.
    """
    match strategy_type:
        case StrategyType.symmetric:
            return SymmetricTokenStrategy(
                access_token_expire_seconds=access_token_expire_seconds,
                secret_key=secret_key,
                algorithm_name=algorithm_name,
            )
        case StrategyType.asymmetric:
            return AsymmetricTokenStrategy(
                access_token_expire_seconds=access_token_expire_seconds,
                secret_key=secret_key,
                algorithm_name=algorithm_name,
                public_key=public_key,
            )
