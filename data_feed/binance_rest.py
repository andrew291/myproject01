import asyncio
import json
import websockets

from config import SYMBOLS
from data_feed.market_state import update_price


BINANCE_WS_URL = "wss://fstream.binance.com/ws/!miniTicker@arr"


async def binance_ws_listener():
    print("Connecting to Binance WebSocket...")

    async with websockets.connect(BINANCE_WS_URL) as websocket:
        print("Connected to Binance WebSocket")

        while True:
            message = await websocket.recv()
            data = json.loads(message)

            for ticker in data:
                symbol = ticker.get("s")
                if symbol not in SYMBOLS:
                    continue

                price = float(ticker.get("c"))
                update_price(symbol, price)


async def start_ws():
    while True:
        try:
            await binance_ws_listener()
        except Exception as e:
            print(f"WebSocket error: {e}")
            print("Reconnecting in 5 seconds...")
            await asyncio.sleep(5)

