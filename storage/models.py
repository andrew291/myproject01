from sqlalchemy import (
    Column,
    Integer,
    String,
    Float,
    DateTime,
    Boolean,
    ForeignKey,
)
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class Signal(Base):
    __tablename__ = "signals"

    id = Column(Integer, primary_key=True, index=True)

    symbol = Column(String, nullable=False)
    timestamp_signal = Column(DateTime, nullable=False)

    direction = Column(String, nullable=False)  # LONG / SHORT
    price_at_signal = Column(Float, nullable=False)
    move_pct = Column(Float, nullable=False)

    volume_1m = Column(Float, nullable=False)
    volume_10m_avg = Column(Float, nullable=False)
    volume_ratio = Column(Float, nullable=False)

    oi = Column(Float, nullable=True)

    buy_vol = Column(Float, nullable=True)
    sell_vol = Column(Float, nullable=True)
    cvd_snapshot = Column(Float, nullable=True)

    ema_side = Column(String, nullable=False)  # above / below
    liquidity_tier = Column(String, nullable=False)  # LOW / HIGH
    cooldown_passed = Column(Boolean, default=True)


class Trade(Base):
    __tablename__ = "trades"

    id = Column(Integer, primary_key=True, index=True)

    signal_id = Column(Integer, ForeignKey("signals.id"), nullable=False)

    symbol = Column(String, nullable=False)
    direction = Column(String, nullable=False)

    entry_delay_seconds = Column(Integer, nullable=False)
    entry_time_planned = Column(DateTime, nullable=False)

    entry_time = Column(DateTime, nullable=True)
    entry_price = Column(Float, nullable=True)

    tp_price = Column(Float, nullable=True)
    sl_price = Column(Float, nullable=True)

    exit_time = Column(DateTime, nullable=True)
    exit_price = Column(Float, nullable=True)
    exit_reason = Column(String, nullable=True)  # TP / SL / TIME

    pnl_pct_1x = Column(Float, nullable=True)
    pnl_pct_5x = Column(Float, nullable=True)

    slippage_used = Column(Float, nullable=True)
    fees_used = Column(Float, nullable=True)

    hold_seconds = Column(Integer, nullable=True)
