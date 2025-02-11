from __future__ import annotations

import httpx

from src.config import settings
from src.db.models import Admin, Channel


class NotificationService:
    @staticmethod
    async def notify_admin(
        admin: Admin, post_id: int, channel: Channel, matched_keywords: set[str],
    ):
        channel_url = channel.url
        if channel_url.startswith("https://t.me/s/"):
            channel_url = f"https://t.me/{channel_url[15:]}"

        channel_str = f"{channel_url}/{post_id}" if channel_url else ""
        text = (
            f"Найден пост на канале: {channel.name or channel_str}\n"
            f"Совпадения: {', '.join(matched_keywords)}\n"
            f"Ссылка: {channel_url}/{post_id}"
        )
        await NotificationService._send_telegram_message(admin.telegram_id, text)

    @staticmethod
    async def _send_telegram_message(chat_id: str, text: str):
        """Отправляет сообщение в Telegram через Bot API.

        :param chat_id: ID чата (Telegram ID администратора).
        :param text: Текст сообщения.
        """
        bot_token = settings.TELEGRAM_BOT_TOKEN

        url = f"https://api.telegram.org/bot{bot_token}/sendMessage"

        payload = {
            "chat_id": chat_id,
            "text": text,
        }

        async with httpx.AsyncClient() as client:
            try:
                response = await client.post(url, json=payload)
                response.raise_for_status()
            except httpx.HTTPStatusError as e:
                print(f"Ошибка при отправке сообщения: {e}")
            except Exception as e:
                print(f"Произошла ошибка: {e}")
