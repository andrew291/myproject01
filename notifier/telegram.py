import asyncio
import urllib.parse
import urllib.request

from config import TELEGRAM_ENABLED, TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID


def _send_telegram_sync(text: str) -> None:
    """
    Synchronous Telegram send using urllib (stdlib).
    Called via asyncio.to_thread() so we don't block the event loop.
    """
    if not TELEGRAM_ENABLED:
        return

    if not TELEGRAM_BOT_TOKEN or "PASTE_" in TELEGRAM_BOT_TOKEN:
        return

    if not TELEGRAM_CHAT_ID or "PASTE_" in str(TELEGRAM_CHAT_ID):
        return

    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": text,
        "disable_web_page_preview": True,
    }

    data = urllib.parse.urlencode(payload).encode("utf-8")
    req = urllib.request.Request(url, data=data, method="POST")

    with urllib.request.urlopen(req, timeout=10) as resp:
        resp.read()


async def send_telegram(text: str) -> None:
    """
    Async wrapper (doesn't crash app on Telegram issues).
    """
    try:
        await asyncio.to_thread(_send_telegram_sync, text)
    except Exception as e:
        print(f"Telegram send failed: {e}")


def futures_link(symbol: str) -> str:
    """
    Binance Futures symbol link format:
    https://www.binance.com/en/futures/BTCUSDT
    """
    return f"https://www.binance.com/en/futures/{symbol}"


def format_signal_message(signal) -> str:
    """
    signal is a SQLAlchemy Signal model instance.
    """
    side = "LONG" if signal.direction.upper() == "LONG" else "SHORT"
    move_pct = signal.move_pct * 100.0
    price = signal.price_at_signal

    return (
        f"📣 SIGNAL: {signal.symbol} | {side}\n"
        f"Move: {move_pct:.2f}% | Price: {price}\n"
        f"Lookback signal id: #{signal.id}\n"
        f"Link: {futures_link(signal.symbol)}"
    )
