from utils.env import load_dotenv
load_dotenv()
import asyncio
from storage.db import init_db
from data_feed.binance_ws import start_ws
from signals.signal_engine import SignalEngine
from trades.trade_simulator import trade_simulator_loop
from trades.signal_consumer import SignalConsumer


async def main():
    print("Initializing database...")
    init_db()
    print("Database initialized.")

    engine = SignalEngine()
    consumer = SignalConsumer()

    await asyncio.gather(
        start_ws(),
        engine.run_forever(),
        consumer.run_forever(),
        trade_simulator_loop(),
    )


if __name__ == "__main__":
    asyncio.run(main())
