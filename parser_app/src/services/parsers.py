from src.services.db import get_keywords
from src.utils.http_requests import fetch_channel_data, get_channel_posts


async def parse_and_match(url: str):
    print(f"Получаем данные с канала: {url}...")
    html = await fetch_channel_data(url)
    if html:

        posts = await get_channel_posts(url)

        keywords = await get_keywords()
        print(keywords)
        print(keywords)

        for post in posts:
            for word, lemma in keywords:
                if word in post.text.lower() or (
                    lemma and lemma in post.text.lower()
                ):
                    print(
                        f"Найдено совпадение: {word} или {lemma} в посте {post.post_id}",
                    )
                else:
                    print(f"Совпадений не найдено в посте {post.post_id} для {word} в {lemma}" )
