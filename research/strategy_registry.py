import logging
from abc import ABC, abstractmethod
from typing import Dict, List, Type

logger = logging.getLogger(__name__)

class BaseStrategy(ABC):
    name: str = "Base"
    version: str = "1.0"

    @abstractmethod
    async def generate_signal(self, market_data: Dict) -> Dict:
        pass

class StrategyRegistry:
    def __init__(self):
        self.strategies = {}

    def register(self, strategy_class: Type[BaseStrategy]):
        strategy = strategy_class()
        self.strategies[strategy.name] = strategy
        logger.info(f"Registered {strategy.name}")

    def get_top_strategies(self):
        return list(self.strategies.values())[:3]