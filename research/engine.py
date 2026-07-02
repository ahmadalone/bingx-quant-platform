import logging
from .strategy_registry import StrategyRegistry, TrendFollowing

logger = logging.getLogger(__name__)

class ResearchEngine:
    """Advanced research with registry."""

    def __init__(self):
        self.registry = StrategyRegistry()
        self.registry.register(TrendFollowing)

    def research(self, data):
        logger.info("Running research...")
        return ["TrendFollowing", "SMC"]

print("Research Engine ready.")