import os

import requests


def send_telegram_message(message):
    bot_token = os.getenv("TELEGRAM_BOT_TOKEN")
    chat_id = os.getenv("TELEGRAM_CHAT_ID")
    
    if not bot_token:
        raise ValueError("Missing TELEGRAM_BOT_TOKEN environment variable")

    if not chat_id:
        raise ValueError("Missing TELEGRAM_CHAT_ID environment variable")

    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"

    payload = {
        "chat_id": chat_id,
        "text": message,
    }

    response = requests.post(
        url,
        json=payload,
        timeout=10,
    )

    response.raise_for_status()

    return response.json()