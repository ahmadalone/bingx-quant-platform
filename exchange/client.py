from bingx import BingXClient
from bingx.websocket import MarketDataStream
from config.settings import settings
import asyncio
import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

class BingXExchange:
    """Institutional-grade BingX API client with real WS support."""

    def __init__(self):
        self.client = BingXClient(
            api_key=settings.BINGX_API_KEY,
            api_secret=settings.BINGX_API_SECRET,
            base_uri='https://open-api.bingx.com' if not settings.BINGX_TESTNET else 'https://open-api-testnet.bingx.com'
        )
        # Real WebSocket
        self.market_stream = MarketDataStream()
        self.market_stream.connect()
        self.subscriptions = []

    async def get_balance(self) -> Dict:
        try:
            balance = self.client.get_balance()
            return balance
        except Exception as e:
            logger.error(f"Balance fetch error: {e}")
            return {}

    async def place_order(self, symbol: str, side: str, quantity: float, price: float = None, order_type: str = "LIMIT"):
        try:
            order = self.client.place_order(symbol=symbol, side=side, quantity=quantity, price=price, type=order_type)
            logger.info(f"Order placed: {order}")
            return order
        except Exception as e:
            logger.error(f"Order error: {e}")
            return None

    def subscribe_market_data(self, symbol: str, channels: list = None):
        if channels is None:
            channels = ["trade", "kline_1m", "depth"]
        for ch in channels:
            if ch == "trade":
                self.market_stream.subscribe_trade(symbol)
            elif ch == "kline_1m":
                self.market_stream.subscribe_kline(symbol, "1m")
        self.market_stream.on_message(self._handle_ws_message)
        logger.info(f"Subscribed to {channels} for {symbol}")

    def _handle_ws_message(self, data):
        logger.info(f"Live WS data received: {data}")
        # Feed to Market Data Engine / EventBus

print("BingX Exchange with real WebSocket ready.")