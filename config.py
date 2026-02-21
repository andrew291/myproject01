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
# Trade Simulation (Paper Trading) — NO TP MODE
# =========================

# Human reaction delay before entry (seconds)
ENTRY_DELAY_SECONDS = 5

# Initial fixed stop loss at entry (percent)
INITIAL_STOP_LOSS_PCT = 0.01   # 1.0%

# Move SL to breakeven once trade is this profitable (percent)
BREAKEVEN_TRIGGER_PCT = 0.005  # 0.5%

# If trade is profitable by at least this amount at TIME_STOP,
# we DO NOT close it — we let trailing SL manage it
PROFITABLE_TIME_BYPASS_PCT = 0.002  # 0.2%

# Trailing stop distance once in profit (percent)
TRAILING_STOP_PCT = 0.004  # 0.4%

# Time-based exit only for non-performing trades
TIME_STOP_SECONDS = 90  # 1.5 minutes

# Absolute max hold time (safety cap)
MAX_HOLD_SECONDS = 300  # 5 minutes

# =========================
# Trailing Stop Logic
# =========================

# Profit required to activate trailing stop
TRAILING_ACTIVATION_PCT = 0.002   # +0.20%

# Distance from peak price
TRAILING_DISTANCE_PCT = 0.0015    # 0.15%


import os

# =========================
# Telegram notifications
# =========================
TELEGRAM_ENABLED = os.getenv("TELEGRAM_ENABLED", "true").lower() in ("1", "true", "yes")

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID", "")

TELEGRAM_NOTIFY_SIGNALS = os.getenv("TELEGRAM_NOTIFY_SIGNALS", "true").lower() in ("1", "true", "yes")

