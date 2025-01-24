from src.services.lemma import find_matches_in_text
from src.services.db import get_keywords
from src.utils.http_requests import fetch_channel_data, get_channel_posts


async def parse_and_match(url: str):
    print(f"Получаем данные с канала: {url}...")
    html = await fetch_channel_data(url)
    if html:
        posts = await get_channel_posts(url)
        keywords = await get_keywords()

        for post in posts:
            matches = find_matches_in_text(post.text, set(keywords))
            if matches:
                print(f"Совпадения в посте {post.post_id}: {matches}")
