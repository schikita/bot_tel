from __future__ import annotations

from datetime import UTC, datetime, timedelta

from src.db.models import Channel


class ChannelRepository:
    @staticmethod
    async def fetch_active_channels() -> list[Channel]:
        return await Channel.filter(is_active=True).all()

    @staticmethod
    async def is_due_for_parsing(channel: Channel) -> bool:
        """Проверяет, истекло ли время до следующего парсинга."""
        return not channel.next_parse_at or channel.next_parse_at < datetime.now(UTC)

    @staticmethod
    async def set_next_parse_time(channel: Channel) -> None:
        next_parse = datetime.now(UTC) + timedelta(minutes=channel.interval_minutes)
        await Channel.filter(id=channel.id).update(next_parse_at=next_parse)
