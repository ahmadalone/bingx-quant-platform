import logging
from typing import Dict
from config.settings import settings

logger = logging.getLogger(__name__)

class RiskEngine:
    """Institutional Risk Management - Protects capital at all costs."""

    def __init__(self):
        self.max_daily_loss = 0.02  # 2%
        self.max_drawdown = 0.10
        self.current_exposure = 0.0
        self.kelly_fraction = 0.5

    def check_trade(self, signal: Dict) -> bool:
        """Pre-trade risk check."""
        if self.current_exposure > 0.8:  # 80% max
            logger.warning("Exposure limit hit. Trade blocked.")
            return False
        return True

    def update_exposure(self, delta: float):
        self.current_exposure += delta
        logger.info(f"Exposure updated: {self.current_exposure:.2%}")

print("Risk Engine initialized.")