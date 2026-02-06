# =========================
# Database
# =========================

DATABASE_URL = "sqlite:///./momentum.db"


# =========================
# Symbols to monitor (Binance USDT Perpetual Futures)
# Carefully selected mix:
# - majors
# - liquid alts
# - volatile movers
# =========================

SYMBOLS = [
    # Majors
    "BTCUSDT",
    "ETHUSDT",
    "BNBUSDT",

    # Large liquid alts
    "SOLUSDT",
    "AVAXUSDT",

    # High-volatility / momentum-friendly
    "DOGEUSDT",
    "PEPEUSDT",
    "TIAUSDT",
    "BLURUSDT",
    "VTHOUSDT",
    "BRETTUSDT",
    "PENGUUSDT",

    # Additional volatile / trending
    "SUIUSDT",
    "HYPEUSDT",
    "BATUSDT",
    "ONEUSDT",
    "BONKUSDT",
    "LPTUSDT",
    "XNOUSDT",
    "FARTCOINUSDT",
    "APTUSDT",
    "WLFIUSDT",
    "ARBUSDT",
    "GIGAUSDT",
    "XECUSDT",
    "POLYXUSDT",
    "TRUMPUSDT",
    "DGBUSDT",
    "ETCUSDT",
    "FLOKIUSDT",
    "ICPUSDT",
]


# =========================
# Signal Engine — Momentum Detection
# (ANALYTICS MODE)
# =========================

# Momentum threshold:
# 0.02 = 2% price move over lookback window
MOMENTUM_PCT = 0.01

# Lookback window for momentum calculation (seconds)
LOOKBACK_SECONDS = 60

# Cooldown per symbol after a signal (seconds)
COOLDOWN_SECONDS = 300  # 5 minutes


# =========================
# Trade Simulation (Paper Trading)
# =========================

ENTRY_DELAY_SECONDS = 5

TAKE_PROFIT_PCT = 0.02   # +2%

STOP_LOSS_PCT = 0.01    # -1%


TIME_STOP_SECONDS = 45  ###

import os

# =========================
# Telegram notifications
# =========================
TELEGRAM_ENABLED = os.getenv("TELEGRAM_ENABLED", "true").lower() in ("1", "true", "yes")

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID", "")

TELEGRAM_NOTIFY_SIGNALS = os.getenv("TELEGRAM_NOTIFY_SIGNALS", "true").lower() in ("1", "true", "yes")

