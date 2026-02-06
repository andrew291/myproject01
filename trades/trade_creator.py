from datetime import datetime, timedelta

from config import ENTRY_DELAY_SECONDS
from storage.queries import create_pending_trade
from data_feed.market_state import market_state


def create_trade_from_signal(signal):
    """
    Create a simulated trade from a signal with human delay.
    """
    symbol = signal.symbol
    direction = signal.direction

    state = market_state.get(symbol)
    if not state or state.price is None:
        return None

    planned_entry_time = datetime.utcnow() + timedelta(seconds=ENTRY_DELAY_SECONDS)

    trade = create_pending_trade(
        signal_id=signal.id,
        symbol=symbol,
        direction=direction,
        entry_delay_seconds=ENTRY_DELAY_SECONDS,
        entry_time_planned=planned_entry_time,
    )

    print(
        f"TRADE CREATED | trade_id={trade.id} | signal_id={signal.id} | "
        f"{symbol} | {direction} | entry_in={ENTRY_DELAY_SECONDS}s"
    )

    return trade
