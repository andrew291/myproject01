import asyncio
from datetime import datetime

from config import (
    TIME_STOP_SECONDS,
    TRAILING_ACTIVATION_PCT,
    TRAILING_DISTANCE_PCT,
)
from storage.queries import (
    get_pending_trades,
    get_open_trades,
    mark_trade_open,
    mark_trade_closed,
)
from data_feed.market_state import market_state


# In-memory trailing state
TRAIL_STATE = {}  # trade_id -> dict


async def trade_simulator_loop():
    print("Trade simulator started (TRAILING MODE).")

    while True:
        now = datetime.utcnow()

        # -------- ENTER TRADES --------
        pending_trades = get_pending_trades()
        for trade in pending_trades:
            if now < trade.entry_time_planned:
                continue

            state = market_state.get(trade.symbol)
            if not state or state.price is None:
                continue

            entry_price = state.price

            mark_trade_open(
                trade_id=trade.id,
                entry_time=now,
                entry_price=entry_price,
                tp_price=None,
                sl_price=None,
            )

            # init trailing state
            TRAIL_STATE[trade.id] = {
                "armed": False,
                "peak_price": entry_price,
            }

            print(
                f"TRADE OPEN | id={trade.id} | {trade.symbol} | {trade.direction} | "
                f"entry={entry_price:.6f}"
            )

        # -------- MANAGE / EXIT TRADES --------
        open_trades = get_open_trades()
        for trade in open_trades:
            state = market_state.get(trade.symbol)
            if not state or state.price is None:
                continue

            price = state.price
            hold_seconds = int((now - trade.entry_time).total_seconds())

            trail = TRAIL_STATE.get(trade.id)
            if trail is None:
                continue

            # --- Update peak price ---
            if trade.direction == "LONG":
                if price > trail["peak_price"]:
                    trail["peak_price"] = price
            else:
                if price < trail["peak_price"]:
                    trail["peak_price"] = price

            # --- Arm trailing stop ---
            if not trail["armed"]:
                pnl = (
                    (price - trade.entry_price) / trade.entry_price
                    if trade.direction == "LONG"
                    else (trade.entry_price - price) / trade.entry_price
                )

                if pnl >= TRAILING_ACTIVATION_PCT:
                    trail["armed"] = True
                    print(
                        f"TRAIL ARMED | trade_id={trade.id} | "
                        f"pnl={pnl*100:.2f}%"
                    )

            exit_reason = None

            # --- Trailing stop logic ---
            if trail["armed"]:
                if trade.direction == "LONG":
                    trail_sl = trail["peak_price"] * (1 - TRAILING_DISTANCE_PCT)
                    if price <= trail_sl:
                        exit_reason = "TRAIL"
                else:
                    trail_sl = trail["peak_price"] * (1 + TRAILING_DISTANCE_PCT)
                    if price >= trail_sl:
                        exit_reason = "TRAIL"

            # --- Time stop ---
            if exit_reason is None and hold_seconds >= TIME_STOP_SECONDS:
                exit_reason = "TIME"

            if exit_reason:
                pnl_1x = (
                    (price - trade.entry_price) / trade.entry_price
                    if trade.direction == "LONG"
                    else (trade.entry_price - price) / trade.entry_price
                )

                pnl_5x = pnl_1x * 5

                mark_trade_closed(
                    trade_id=trade.id,
                    exit_time=now,
                    exit_price=price,
                    exit_reason=exit_reason,
                    pnl_pct_1x=pnl_1x,
                    pnl_pct_5x=pnl_5x,
                    slippage_used=0.0,
                    fees_used=0.0,
                    hold_seconds=hold_seconds,
                )

                TRAIL_STATE.pop(trade.id, None)

                print(
                    f"TRADE CLOSED | id={trade.id} | reason={exit_reason} | "
                    f"pnl_1x={pnl_1x*100:.2f}% | hold={hold_seconds}s"
                )

        await asyncio.sleep(1)
