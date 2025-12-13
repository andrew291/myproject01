from collections import deque
from typing import Dict
from datetime import datetime


# How many seconds of price history we keep
PRICE_HISTORY_SECONDS = 120


class MarketSymbolState:
    def __init__(self):
        self.price: float | None = None
        self.last_update: datetime | None = None

        # deque of (timestamp, price)
        self.price_history = deque(maxlen=PRICE_HISTORY_SECONDS)


# Global market state
market_state: Dict[str, MarketSymbolState] = {}


def init_symbol(symbol: str):
    if symbol not in market_state:
        market_state[symbol] = MarketSymbolState()


def update_price(symbol: str, price: float):
    init_symbol(symbol)

    now = datetime.utcnow()
    state = market_state[symbol]

    state.price = price
    state.last_update = now
    state.price_history.append((now, price))


def get_latest_price(symbol: str) -> float | None:
    state = market_state.get(symbol)
    if not state:
        return None
    return state.price

