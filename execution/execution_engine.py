import asyncio
import logging
from .order_manager import OrderManager
from risk.engine import RiskEngine

logger = logging.getLogger(__name__)

class ExecutionEngine:
    """Institutional execution."""

    def __init__(self, exchange, risk: RiskEngine):
        self.exchange = exchange
        self.risk = risk
        self.order_manager = OrderManager()

    async def execute_signal(self, signal: dict):
        if not self.risk.check_trade(signal):
            return
        order = await self.order_manager.place_order(signal, self.exchange)
        print("Signal executed.")