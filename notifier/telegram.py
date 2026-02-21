import os
import json
import asyncio
import urllib.parse
import urllib.request


def _env_bool(name: str, default: bool = False) -> bool:
    v = os.getenv(name)
    if v is None:
        return default
    return v.strip().lower() in ("1", "true", "yes", "on")


def _send_telegram_sync(text: str) -> None:
    """
    Synchronous send via Telegram Bot API.
    Reads env vars at runtime so it works after load_dotenv() in main.py.
    """
    enabled = _env_bool("TELEGRAM_ENABLED", False)
    notify_signals = _env_bool("TELEGRAM_NOTIFY_SIGNALS", True)

    if not enabled or not notify_signals:
        return

    token = os.getenv("TELEGRAM_BOT_TOKEN")
    chat_id = os.getenv("TELEGRAM_CHAT_ID")

    if not token or not chat_id:
        raise RuntimeError(
            "Telegram env not set. Need TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID in .env"
        )

    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {"chat_id": chat_id, "text": text}

    data = urllib.parse.urlencode(payload).encode("utf-8")

    req = urllib.request.Request(
        url,
        data=data,
        headers={"Content-Type": "application/x-www-form-urlencoded"},
        method="POST",
    )

    with urllib.request.urlopen(req, timeout=10) as resp:
        body = resp.read().decode("utf-8")
        parsed = json.loads(body)
        if not parsed.get("ok"):
            raise RuntimeError(f"Telegram API error: {body}")


async def send_telegram(text: str) -> None:
    """
    Async wrapper so we don't block the event loop.
    """
    try:
        await asyncio.to_thread(_send_telegram_sync, text)
    except Exception as e:
        print(f"Telegram send failed: {e}")


def format_signal_message(signal) -> str:
    """
    Keep it simple. You can expand later.
    """
    move_pct = getattr(signal, "move_pct", 0.0) * 100.0
    return (
        f"📈 SIGNAL #{signal.id}\n"
        f"{signal.symbol} | {signal.direction}\n"
        f"move={move_pct:.2f}% | price={signal.price_at_signal}\n"
        f"time={signal.timestamp_signal}"
    )
