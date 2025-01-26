from __future__ import annotations

from src.db.models import Admin, Channel


class AdminRepository:
    @staticmethod
    async def get_subscribed_admins(channel: Channel) -> list[Admin]:
        """Возвращает список админов, подписанных на указанный канал."""
        return await channel.admins.all().prefetch_related("words")
