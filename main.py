import asyncio
from datetime import datetime

from data_feed.binance_ws import start_ws
from data_feed.market_state import market_state
from config import SYMBOLS


async def printer():
    while True:
        await asyncio.sleep(5)

        print("\n--- MARKET SNAPSHOT ---")
        for symbol in SYMBOLS:
            state = market_state.get(symbol)
            if not state or state.price is None:
                continue

            print(
                f"{symbol} | price={state.price} | "
                f"points={len(state.price_history)} | "
                f"last={state.last_update}"
            )


async def main():
    ws_task = asyncio.create_task(start_ws())
    printer_task = asyncio.create_task(printer())

    await asyncio.gather(ws_task, printer_task)


if __name__ == "__main__":
    asyncio.run(main())
