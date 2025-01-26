from __future__ import annotations

from datetime import UTC, datetime

from src.db.models import Channel, Post


class PostRepository:
    @staticmethod
    async def create_post(
        channel: Channel,
        post_id: int,
        text: str,
        published_at,
    ) -> Post:
        return await Post.create(
            channel=channel,
            post_id=post_id,
            text=text,
            published_at=published_at,
            created_at=datetime.now(UTC),
        )

    @staticmethod
    async def is_post_exists(channel: Channel, post_id: int) -> bool:
        return await Post.exists(channel=channel, post_id=post_id)
