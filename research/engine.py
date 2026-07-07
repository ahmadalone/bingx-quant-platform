import logging
from .strategy_registry import StrategyRegistry
from .strategies.trend import TrendFollowing

logger = logging.getLogger(__name__)

class ResearchEngine:
    """Advanced research."""

    def __init__(self):
        self.registry = StrategyRegistry()
        self.registry.register(TrendFollowing)

    def research(self, data):
        logger.info("Research running...")
        return self.registry.get_top_strategies()

# No top-level print