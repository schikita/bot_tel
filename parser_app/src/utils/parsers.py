from src.utils.http_requests import fetch_channel_data, get_channel_posts
from src.utils.services import get_keywords


async def parse_and_match(url: str):
    print(f"Получаем данные с канала: {url}...")
    html = await fetch_channel_data(url)
    if html:

        posts = await get_channel_posts(url)

        keywords = await get_keywords()

        for post in posts:
            for word, lemma in keywords:
                if word in post["text"].lower() or (
                    lemma and lemma in post["text"].lower()
                ):
                    print(
                        f"Найдено совпадение: {word} или {lemma} в посте {post['post_id']}"
                    )
