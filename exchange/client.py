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
        self.market_stream = MarketDataStream()
        try:
            self.market_stream.connect()
        except Exception as e:
            logger.warning(f"Initial WS connect: {e}")

    async def get_balance(self) -> Dict:
        try:
            balance = self.client.account()
            return balance
        except Exception as e:
            logger.error(f"Balance fetch error: {e}")
            return {}

    def subscribe_market_data(self, symbol: str, channels: list = None):
        if channels is None:
            channels = ["trade", "kline_1m"]
        try:
            if not getattr(self.market_stream, 'ws', None) or not self.market_stream.ws.connected:
                self.market_stream.connect()
            for ch in channels:
                if ch == "trade":
                    self.market_stream.subscribe_trade(symbol)
                elif ch == "kline_1m":
                    self.market_stream.subscribe_kline(symbol, "1m")
            self.market_stream.on_message(self._handle_ws_message)
            logger.info(f"Subscribed to live data for {symbol}")
        except Exception as e:
            logger.error(f"WS subscription error: {e}")

    def _handle_ws_message(self, data):
        logger.info(f"Live WS data: {data}")

print("BingX Exchange with real WS ready.")