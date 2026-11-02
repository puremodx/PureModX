"""PureModX Image Bot — Telegram polling foundation.

Set BOT_TOKEN in the hosting provider's environment variables.
Do not commit real credentials to GitHub.
"""
import logging
import os
import time
from typing import Any

import requests

BOT_TOKEN = os.getenv("BOT_TOKEN", "YOUR_BOT_TOKEN").strip()
if not BOT_TOKEN:
    raise RuntimeError("BOT_TOKEN is missing. Set it in your hosting environment.")

API_BASE = f"https://api.telegram.org/bot{BOT_TOKEN}/"
HTTP = requests.Session()
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
)
log = logging.getLogger("puremodx-imagebot")


def telegram(method: str, payload: dict[str, Any] | None = None) -> dict[str, Any]:
    """Call the Telegram Bot API and return its JSON response."""
    response = HTTP.post(API_BASE + method, json=payload or {}, timeout=45)
    response.raise_for_status()
    data = response.json()
    if not data.get("ok"):
        raise RuntimeError(f"Telegram API error: {data}")
    return data


def send_message(chat_id: int, text: str) -> None:
    telegram("sendMessage", {"chat_id": chat_id, "text": text})


def handle_message(message: dict[str, Any]) -> None:
    chat = message.get("chat") or {}
    chat_id = chat.get("id")
    text = (message.get("text") or "").strip()
    if not chat_id or not text:
        return

    if text == "/start":
        send_message(
            chat_id,
            "🎨 Welcome to PureModX Image Generator!\n\n"
            "Send an image prompt to get started.\n"
            "Use /help to see available commands.",
        )
    elif text == "/help":
        send_message(
            chat_id,
            "📝 Send a text prompt to request an image.\n"
            "Use /cancel to clear your current request.\n\n"
            "Image generation is not connected yet.",
        )
    elif text == "/cancel":
        send_message(chat_id, "✅ Nothing is currently generating.")
    elif text.startswith("/"):
        send_message(chat_id, "Unknown command. Send /help.")
    else:
        # Generator integration will be added only through an authorized API.
        send_message(
            chat_id,
            "✅ Prompt received:\n\n"
            f"{text[:3000]}\n\n"
            "⚙️ Image generation is not connected yet.",
        )


def main() -> None:
    log.info("PureModX Image Bot starting")
    offset: int | None = None

    while True:
        try:
            result = telegram(
                "getUpdates",
                {"offset": offset, "timeout": 30, "allowed_updates": ["message"]},
            )
            for update in result.get("result", []):
                offset = update["update_id"] + 1
                try:
                    message = update.get("message")
                    if message:
                        handle_message(message)
                except Exception:
                    log.exception("Failed to process update %s", update.get("update_id"))
        except (requests.RequestException, RuntimeError, ValueError):
            log.exception("Telegram polling failed; retrying in 5 seconds")
            time.sleep(5)


if __name__ == "__main__":
    main()
