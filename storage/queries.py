from datetime import datetime
from typing import List, Optional

from sqlalchemy.orm import Session
from sqlalchemy import select

from storage.db import SessionLocal
from storage.models import Signal, Trade


# ---------- SIGNAL QUERIES ----------

def insert_signal(signal_data: dict) -> Signal:
    session: Session = SessionLocal()
    try:
        signal = Signal(**signal_data)
        session.add(signal)
        session.commit()
        session.refresh(signal)
        return signal
    finally:
        session.close()


def get_signal_by_id(signal_id: int) -> Optional[Signal]:
    session: Session = SessionLocal()
    try:
        return session.query(Signal).filter(Signal.id == signal_id).first()
    finally:
        session.close()


def get_signals_without_trade(
    since_time: datetime,
    limit: int = 100,
) -> List[Signal]:
    """
    Return signals newer than since_time that do NOT yet have a trade row.
    This is used by SignalConsumer to create exactly one trade per signal.
    """
    session: Session = SessionLocal()
    try:
        used_signal_ids_sel = select(Trade.signal_id)

        rows = (
            session.query(Signal)
            .filter(Signal.timestamp_signal >= since_time)
            .filter(~Signal.id.in_(used_signal_ids_sel))
            .order_by(Signal.id.asc())
            .limit(limit)
            .all()
        )
        return rows
    finally:
        session.close()


def trade_exists_for_signal(signal_id: int) -> bool:
    """
    Safety check to prevent duplicate trades for a signal.
    Useful across restarts and protects against race conditions.
    """
    session: Session = SessionLocal()
    try:
        return session.query(Trade).filter(Trade.signal_id == signal_id).first() is not None
    finally:
        session.close()


# ---------- TRADE QUERIES ----------

def create_pending_trade(
    signal_id: int,
    symbol: str,
    direction: str,
    entry_delay_seconds: int,
    entry_time_planned: datetime,
) -> Trade:
    session: Session = SessionLocal()
    try:
        trade = Trade(
            signal_id=signal_id,
            symbol=symbol,
            direction=direction,
            entry_delay_seconds=entry_delay_seconds,
            entry_time_planned=entry_time_planned,
        )
        session.add(trade)
        session.commit()
        session.refresh(trade)
        return trade
    finally:
        session.close()


def get_pending_trades() -> List[Trade]:
    session: Session = SessionLocal()
    try:
        return (
            session.query(Trade)
            .filter(Trade.entry_time.is_(None))
            .all()
        )
    finally:
        session.close()


def mark_trade_open(
    trade_id: int,
    entry_time: datetime,
    entry_price: float,
    tp_price: Optional[float],
    sl_price: float,
):
    session: Session = SessionLocal()
    try:
        trade = session.query(Trade).filter(Trade.id == trade_id).first()
        if trade is None:
            return

        trade.entry_time = entry_time
        trade.entry_price = entry_price
        trade.tp_price = tp_price  # can be None in NO-TP mode
        trade.sl_price = sl_price

        session.commit()
    finally:
        session.close()


def update_trade_sl(trade_id: int, new_sl_price: float):
    """
    Update SL while trade is open (breakeven / trailing).
    """
    session: Session = SessionLocal()
    try:
        trade = session.query(Trade).filter(Trade.id == trade_id).first()
        if trade is None:
            return
        trade.sl_price = new_sl_price
        session.commit()
    finally:
        session.close()


def get_open_trades() -> List[Trade]:
    session: Session = SessionLocal()
    try:
        return (
            session.query(Trade)
            .filter(Trade.entry_time.isnot(None))
            .filter(Trade.exit_time.is_(None))
            .all()
        )
    finally:
        session.close()


def mark_trade_closed(
    trade_id: int,
    exit_time: datetime,
    exit_price: float,
    exit_reason: str,
    pnl_pct_1x: float,
    pnl_pct_5x: float,
    slippage_used: float,
    fees_used: float,
    hold_seconds: int,
):
    session: Session = SessionLocal()
    try:
        trade = session.query(Trade).filter(Trade.id == trade_id).first()
        if trade is None:
            return

        trade.exit_time = exit_time
        trade.exit_price = exit_price
        trade.exit_reason = exit_reason
        trade.pnl_pct_1x = pnl_pct_1x
        trade.pnl_pct_5x = pnl_pct_5x
        trade.slippage_used = slippage_used
        trade.fees_used = fees_used
        trade.hold_seconds = hold_seconds

        session.commit()
    finally:
        session.close()
