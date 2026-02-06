import asyncio
from datetime import datetime

from config import TAKE_PROFIT_PCT, STOP_LOSS_PCT, TIME_STOP_SECONDS
from storage.queries import (
    get_pending_trades,
    get_open_trades,
    mark_trade_open,
    mark_trade_closed,
)
from data_feed.market_state import market_state


async def trade_simulator_loop():
    print("Trade simulator started.")

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

            if trade.direction == "LONG":
                tp_price = entry_price * (1 + TAKE_PROFIT_PCT)
                sl_price = entry_price * (1 - STOP_LOSS_PCT)
            else:
                tp_price = entry_price * (1 - TAKE_PROFIT_PCT)
                sl_price = entry_price * (1 + STOP_LOSS_PCT)

            mark_trade_open(
                trade_id=trade.id,
                entry_time=now,
                entry_price=entry_price,
                tp_price=tp_price,
                sl_price=sl_price,
            )

            print(
                f"TRADE OPEN | id={trade.id} | {trade.symbol} | {trade.direction} | "
                f"entry={entry_price:.6f} | tp={tp_price:.6f} | sl={sl_price:.6f}"
            )

        # -------- EXIT TRADES --------
        open_trades = get_open_trades()
        for trade in open_trades:
            state = market_state.get(trade.symbol)
            if not state or state.price is None:
                continue

            price = state.price
            hold_seconds = int((now - trade.entry_time).total_seconds())

            exit_reason = None

            if trade.direction == "LONG":
                if price >= trade.tp_price:
                    exit_reason = "TP"
                elif price <= trade.sl_price:
                    exit_reason = "SL"
            else:
                if price <= trade.tp_price:
                    exit_reason = "TP"
                elif price >= trade.sl_price:
                    exit_reason = "SL"

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

                print(
                    f"TRADE CLOSED | id={trade.id} | reason={exit_reason} | "
                    f"pnl_1x={pnl_1x*100:.2f}% | pnl_5x={pnl_5x*100:.2f}% | "
                    f"hold={hold_seconds}s"
                )

        await asyncio.sleep(1)
