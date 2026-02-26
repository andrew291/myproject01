🚀 Crypto Momentum Signal & Trade Simulator

A modular, end-to-end crypto market signal → trade simulation system built in Python.

This project connects to Binance Futures WebSocket, detects momentum-based trading signals, converts them into simulated trades, tracks performance, and optionally sends Telegram notifications.

✅ Requirements

Python 3.10+ (required — project uses modern type hints like float | None)

Internet connection (for Binance WebSocket)

Optional: Telegram bot credentials

✨ Key Features

📡 Real-time Binance Futures WebSocket feed

📊 Momentum-based signal engine (configurable)

🔁 Signal → Trade pipeline (exactly one trade per signal)

🧪 Trade simulator (TP / SL / time-based exits)

🗃️ SQLite storage (signals + trades)

📬 Telegram notifications for trade suggestions

🧩 Pluggable strategy logic (easy to extend)

🧠 Analytics-ready data model

--- 

## 🧠 Architecture Overview

mermaid
flowchart TD
    WS[Binance WebSocket] --> MS[Market State]
    MS --> SE[Signal Engine]
    SE -->|signal| DB[(SQLite)]
    DB --> SC[Signal Consumer]
    SC --> TC[Trade Creator]
    TC --> TS[Trade Simulator]
    TS --> DB
    SE -->|notify| TG[Telegram]

---

📁 Project Structure
myproject01/
├── analytics/           # notebooks & analysis (future)
├── data_feed/           # Binance WS + market state
├── notifier/            # Telegram integration
├── signals/             # Signal engines & filters
├── storage/             # DB models & queries
├── trades/              # Trade creation & simulation
├── utils/               # env / helpers
├── scripts/             # Windows setup & run scripts
├── config.py            # Strategy & system config
├── main.py              # App entrypoint
├── requirements.txt     # Dependencies
├── .env.example         # Environment variable template
├── .gitignore
└── README.md
⚙️ Configuration

All strategy behavior is controlled via config.py.

Key parameters:

# Momentum signal parameters
MOMENTUM_PCT = 0.02        # 2% move threshold
LOOKBACK_SECONDS = 120     # price lookback window
COOLDOWN_SECONDS = 300     # per-symbol cooldown

# Trade simulation
ENTRY_DELAY_SECONDS = 5
TAKE_PROFIT_PCT = 0.02
STOP_LOSS_PCT = 0.01
TIME_STOP_SECONDS = 90

Symbols are also configurable:

SYMBOLS = [
    "BTCUSDT", "ETHUSDT", "SOLUSDT", "AVAXUSDT",
    "DOGEUSDT", "PEPEUSDT", "TIAUSDT", "BLURUSDT",
]
🔔 Telegram Notifications

The system can notify you when a trade is suggested.

Setup

Create a local .env file:

cp .env.example .env

Fill in your values:

TELEGRAM_ENABLED=true
TELEGRAM_NOTIFY_SIGNALS=true
TELEGRAM_BOT_TOKEN=PASTE_TOKEN_HERE
TELEGRAM_CHAT_ID=PASTE_CHAT_ID_HERE

Open your bot in Telegram and press Start.

⚠️ Never commit real tokens — .env is ignored by git.

▶️ Running Locally

Requires Python 3.10+

🪟 Windows (PowerShell)
1️⃣ Install Python (one-time)

Download Python 3.10+ from:
https://www.python.org/downloads/windows/

During installation:

✅ Check “Add Python to PATH”

✅ Ensure pip is installed

Verify:

python --version
python -m pip --version
2️⃣ Clone the repository
git clone https://github.com/andrew291/myproject01.git
cd myproject01
3️⃣ Allow running local scripts (first time only)
Set-ExecutionPolicy -Scope CurrentUser RemoteSigned

Press Y to confirm.

4️⃣ Setup environment
.\scripts\setup.ps1

This will:

Create .venv

Install dependencies

Prepare environment

5️⃣ Run the application
.\scripts\run.ps1

Stop with Ctrl + C.

🍎 macOS (Terminal)
1️⃣ Check Python version
python3 --version

If version is lower than 3.10, install Python 3.10+ from:

https://www.python.org/downloads/macos/

Restart Terminal after installation.

Verify again:

python3 --version
2️⃣ Clone the repository
git clone https://github.com/andrew291/myproject01.git
cd myproject01
3️⃣ Create virtual environment
python3 -m venv .venv
source .venv/bin/activate
4️⃣ Install dependencies
pip install -r requirements.txt

(Optional but recommended)

python -m pip install --upgrade pip
5️⃣ Configure Telegram (optional)
cp .env.example .env

Edit .env with your credentials.

6️⃣ Run the application
python main.py

Stop with Ctrl + C.

You should see:

Initializing database...
Database initialized.
Connecting to Binance WebSocket...
SignalEngine started.
SignalConsumer started.
Trade simulator started.
Connected to Binance WebSocket
🧪 Strategy Logic

Currently implemented:

Pure momentum strategy

Long if price ↑ above threshold

Short if price ↓ below threshold

A generic trade-creation layer is already in place, meaning:

🔁 You can change how trades are created without touching the rest of the system.

Examples of future logic:

mean-reversion (fade strong moves)

SMA / EMA trend filters

volume-confirmed breakouts

regime-based strategies

📊 Analytics & Data

All signals and trades are stored in SQLite:

signals table — raw signal events

trades table — simulated execution & PnL

You can export data easily:

sqlite3 momentum.db ".headers on" ".mode csv" "select * from trades;" > trades.csv

Perfect for:

Jupyter notebooks

Pandas analysis

Strategy evaluation

🗺️ Roadmap Ideas

📈 SMA / EMA trend filters

📊 Post-trade analytics module

🧠 Strategy comparison framework

🔄 Multiple strategies sharing same data feed

🧪 A/B testing via Telegram notifications

📉 Drawdown & risk metrics

⚠️ Disclaimer

This project is for educational and research purposes only.

No real trading is performed

No financial advice

Use at your own risk

⭐ Final Note

This repository is intentionally designed as a clean, extensible foundation.

You are encouraged to:

fork it

modify strategy logic

experiment freely

Happy hacking 🚀