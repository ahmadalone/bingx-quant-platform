import asyncio
import logging
from typing import Dict
from .rest import BingXRestClient
from .websocket import BingXWebSocket
from config.settings import settings

logger = logging.getLogger(__name__)

class BingXExchange:
    """Production BingX adapter."""

    def __init__(self):
        self.rest = BingXRestClient(api_key=settings.BINGX_API_KEY, api_secret=settings.BINGX_API_SECRET)
        self.ws = BingXWebSocket()

    async def connect(self):
        await self.ws.connect()

    async def get_balance(self):
        return await self.rest.get_balance()

    async def subscribe_market_data(self, symbol: str):
        await self.ws.subscribe(f"{symbol}@trade")
        self.ws.set_handler(lambda d: logger.info(f"WS: {d}"))
        logger.info(f"Subscribed to {symbol}")