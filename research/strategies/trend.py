from ..strategy_registry import BaseStrategy
from typing import Dict

class TrendFollowing(BaseStrategy):
    name = "TrendFollowing"

    async def generate_signal(self, market_data: Dict) -> Dict:
        return {"direction": "LONG", "confidence": 0.82, "reasons": ["EMA crossover"]}