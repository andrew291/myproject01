import asyncio
from datetime import datetime

from storage.queries import get_signals_without_trade, trade_exists_for_signal
from trades.trade_creator import create_trade_from_signal


class SignalConsumer:
    """
    Consumes signals from DB and creates one pending trade per signal.

    IMPORTANT:
    - Only consumes signals created AFTER startup_time (no backfill).
    - Prevents duplicates by checking existing trades.
    """

    def __init__(self):
        self.startup_time = datetime.utcnow()

    async def run_forever(self):
        print("SignalConsumer started (signals -> trades).")

        while True:
            try:
                signals = get_signals_without_trade(self.startup_time, limit=200)

                for sig in signals:
                    if trade_exists_for_signal(sig.id):
                        continue

                    trade = create_trade_from_signal(sig)
                    if trade is None:
                        continue

                await asyncio.sleep(1)

            except Exception as e:
                print(f"SignalConsumer error: {e}")
                await asyncio.sleep(2)

