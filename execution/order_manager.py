import logging
from uuid import uuid4
from typing import Dict, Optional

logger = logging.getLogger(__name__)

class OrderManager:
    """Idempotent order manager."""

    def __init__(self):
        self.pending_orders = {}

    async def place_order(self, signal: Dict, exchange_client) -> Optional[Dict]:
        signal_id = signal.get("id") or str(uuid4())
        if signal_id in self.pending_orders:
            logger.warning("Duplicate order blocked")
            return None
        self.pending_orders[signal_id] = signal
        try:
            order = await exchange_client.place_order(
                symbol=signal.get("symbol"),
                side=signal.get("side"),
                quantity=signal.get("quantity", 0.001)
            )
            return order
        except Exception as e:
            logger.error(f"Order failed: {e}")
            del self.pending_orders[signal_id]
            return None