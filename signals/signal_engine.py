import asyncio
from datetime import datetime, timedelta

from config import SYMBOLS, MOMENTUM_PCT, LOOKBACK_SECONDS, COOLDOWN_SECONDS, TELEGRAM_NOTIFY_SIGNALS
from data_feed.market_state import market_state
from storage.queries import insert_signal
from notifier.telegram import send_telegram, format_signal_message


def _find_price_at_or_before(symbol: str, target_time: datetime):
    """
    Find the last price in the symbol's history with timestamp <= target_time.
    Returns None if not found.
    """
    state = market_state.get(symbol)
    if not state or not state.price_history:
        return None

    chosen_price = None
    for ts, price in state.price_history:
        if ts <= target_time:
            chosen_price = price
        else:
            break
    return chosen_price


class SignalEngine:
    def __init__(self):
        self._last_signal_time = {} 

    def _cooldown_passed(self, symbol: str, now: datetime) -> bool:
        last = self._last_signal_time.get(symbol)
        if last is None:
            return True
        return (now - last).total_seconds() >= COOLDOWN_SECONDS

    def _mark_signaled(self, symbol: str, now: datetime):
        self._last_signal_time[symbol] = now

    async def run_forever(self):
        print("SignalEngine started (Option 1: pure momentum).")

        while True:
            now = datetime.utcnow()
            lookback_time = now - timedelta(seconds=LOOKBACK_SECONDS)

            for symbol in SYMBOLS:
                state = market_state.get(symbol)
                if not state or state.price is None:
                    continue

                old_price = _find_price_at_or_before(symbol, lookback_time)
                if old_price is None or old_price <= 0:
                    continue

                current_price = state.price
                move_pct = (current_price - old_price) / old_price

                if abs(move_pct) < MOMENTUM_PCT:
                    continue

                if not self._cooldown_passed(symbol, now):
                    continue

                direction = "LONG" if move_pct > 0 else "SHORT"


                signal_data = {
                    "symbol": symbol,
                    "timestamp_signal": now,
                    "direction": direction,
                    "price_at_signal": float(current_price),
                    "move_pct": float(move_pct),

                    "volume_1m": 0.0,
                    "volume_10m_avg": 0.0,
                    "volume_ratio": 0.0,
                    "oi": None,
                    "buy_vol": None,
                    "sell_vol": None,
                    "cvd_snapshot": None,
                    "ema_side": "unknown",
                    "liquidity_tier": "HIGH",
                    "cooldown_passed": True,
                }

                saved = insert_signal(signal_data)
                self._mark_signaled(symbol, now)

                print(
                    f"SIGNAL #{saved.id} | {symbol} | {direction} | "
                    f"move={move_pct*100:.2f}% | price={current_price} | "
                    f"lookback={LOOKBACK_SECONDS}s"
                )

                if TELEGRAM_NOTIFY_SIGNALS:
                    await send_telegram(format_signal_message(saved))

            await asyncio.sleep(1)
