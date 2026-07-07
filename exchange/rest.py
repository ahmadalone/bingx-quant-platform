import asyncio
import hashlib
import hmac
import time
from urllib.parse import urlencode
import aiohttp
import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

class BingXRestClient:
    """Self-contained REST client for BingX."""

    def __init__(self, api_key: str, api_secret: str, base_url: str = "https://open-api.bingx.com"):
        self.api_key = api_key
        self.api_secret = api_secret
        self.base_url = base_url
        self.session = None

    async def _get_session(self):
        if self.session is None:
            self.session = aiohttp.ClientSession()
        return self.session

    def _sign(self, params: Dict = None) -> str:
        if not params:
            params = {}
        params = params.copy()
        params['timestamp'] = int(time.time() * 1000)
        query = urlencode(sorted(params.items()))
        signature = hmac.new(self.api_secret.encode(), query.encode(), hashlib.sha256).hexdigest()
        return query + '&signature=' + signature

    async def request(self, method: str, endpoint: str, params: Dict = None, signed: bool = False, json_body: bool = False) -> Dict:
        for attempt in range(3):
            try:
                session = await self._get_session()
                url = f"{self.base_url}{endpoint}"
                headers = {'Content-Type': 'application/json'} if json_body else None
                data = None
                if signed:
                    full_query = self._sign(params)
                    url += '?' + full_query
                elif params and method.upper() == 'POST':
                    data = params
                async with session.request(method, url, params=params if not signed and method.upper() == 'GET' else None, json=data if json_body else None, data=data if not json_body else None, headers=headers, timeout=10) as resp:
                    data_resp = await resp.json()
                    if data_resp.get('code') == 0:
                        return data_resp.get('data', data_resp)
                    else:
                        logger.error(f"BingX error: {data_resp}")
                        return {}
            except Exception as e:
                logger.warning(f"Request attempt {attempt}: {e}")
                await asyncio.sleep(2 ** attempt)
        return {}

    async def get_balance(self):
        return await self.request('GET', '/openApi/swap/v2/user/balance', signed=True)

    async def place_order(self, symbol, side, qty, price=None, order_type="LIMIT"):
        params = {"symbol": symbol, "side": side, "quantity": str(qty), "type": order_type}
        if price:
            params["price"] = str(price)
        # For POST, use signed query
        return await self.request('POST', '/openApi/swap/v2/trade/order', params, signed=True)