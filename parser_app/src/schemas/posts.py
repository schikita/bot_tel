from __future__ import annotations

from datetime import UTC, datetime

from pydantic import BaseModel


class PostData(BaseModel):
    post_id: int
    text: str
    published_at: str | None = datetime.now(UTC).isoformat()


class PostsResponse(BaseModel):
    posts: list[PostData]
