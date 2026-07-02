import asyncio
import json
import logging
import websockets
from typing import Callable

logger = logging.getLogger(__name__)

class BingXWebSocket:
    """Production WS manager."""

    def __init__(self):
        self.ws = None
        self.uri = "wss://open-api-swap.bingx.com/swap-ws"
        self.subscriptions = []
        self.message_handler = None
        self.running = False

    async def connect(self):
        for attempt in range(5):
            try:
                self.ws = await websockets.connect(self.uri)
                self.running = True
                asyncio.create_task(self._listen())
                logger.info("WebSocket connected.")
                await self._resubscribe()
                return
            except Exception as e:
                logger.warning(f"WS attempt {attempt}: {e}")
                await asyncio.sleep(2 ** attempt)
        logger.error("WS connect failed.")

    async def _listen(self):
        while self.running and self.ws:
            try:
                msg = await self.ws.recv()
                data = json.loads(msg)
                if self.message_handler:
                    self.message_handler(data)
            except Exception as e:
                logger.error(f"WS listen: {e}")
                break
        await self.reconnect()

    async def reconnect(self):
        await self.connect()

    async def subscribe(self, topic: str):
        self.subscriptions.append(topic)
        if self.ws:
            await self.ws.send(json.dumps({"op": "subscribe", "args": [{"channel": topic}]}))
            logger.info(f"Subscribed {topic}")

    def set_handler(self, handler: Callable):
        self.message_handler = handler

    async def _resubscribe(self):
        for topic in self.subscriptions:
            await self.subscribe(topic)

    async def close(self):
        self.running = False
        if self.ws:
            await self.ws.close()