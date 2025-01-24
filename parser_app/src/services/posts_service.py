from typing import List

from src.db.models import Post
from src.schemas.posts import PostSchema
from src.services.lemma import find_matches_in_text
from src.services.parsers import get_keywords


async def get_posts_from_db() -> List[PostSchema]:
    posts_from_db = await Post.all().values(
        "post_id",
        "text",
    )
    return [PostSchema(**post) for post in posts_from_db]


async def parse_and_match(channel_url: str):
    print(f"Получаем данные с канала: {channel_url}...")
    posts = await get_posts_from_db()

    keywords = await get_keywords()

    keyword_set = set(lemma for word, lemma in keywords)

    for post in posts:
        matched_keywords = find_matches_in_text(post.text, keyword_set)
        if matched_keywords:
            print(
                f"Найдено совпадение: {', '.join(matched_keywords)} в посте {post.post_id}",
            )
