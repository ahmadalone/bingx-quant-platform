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
    await exchange.connect()  # New
    research = ResearchEngine()
    risk = RiskEngine()
    execution = ExecutionEngine(exchange, risk)

    balance = await exchange.get_balance()
    print("Balance:", balance)

    exchange.subscribe_market_data("BTC-USDT")

    strategies = research.research(None)
    print("Top strategies:", strategies)

    sample_signal = {"id": "sig1", "side": "BUY", "symbol": "BTC-USDT", "quantity": 0.001, "confidence": 0.85}
    await execution.execute_signal(sample_signal)

    print("Full Platform with improved execution started.")

if __name__ == "__main__":
    asyncio.run(main())