import asyncio
import logging
from config.settings import settings
from exchange.client import BingXExchange
from research.engine import ResearchEngine
from risk.engine import RiskEngine
from execution.execution_engine import ExecutionEngine

logging.basicConfig(level=logging.INFO)

async def main():
    exchange = BingXExchange()
    await exchange.connect()
    research = ResearchEngine()
    risk = RiskEngine()
    execution = ExecutionEngine(exchange, risk)

    balance = await exchange.get_balance()
    print("Balance:", balance)

    exchange.subscribe_market_data("BTC-USDT")

    strategies = research.research(None)
    print("Top strategies:", strategies)

    sample_signal = {"id": "sig1", "side": "BUY", "symbol": "BTC-USDT", "quantity": 0.001}
    await execution.execute_signal(sample_signal)

    print("Platform with advanced research started.")

if __name__ == "__main__":
    asyncio.run(main())