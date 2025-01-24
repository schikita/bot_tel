from src.services.lemma import find_matches_in_text
from src.services.db import get_keywords
from src.utils.http_requests import fetch_channel_data, get_channel_posts
from src.services.lemma import lemmatize_word

async def parse_and_match(url: str):
    print(f"Получаем данные с канала: {url}...")
    html = await fetch_channel_data(url)
    if html:
        posts = await get_channel_posts(url)  # Получаем все посты
        keywords = await get_keywords()  # Получаем все ключевые слова
        print("Ключевые слова:", keywords)

        # Лемматизация ключевых слов
        lemmatized_keywords = {lemmatize_word(keyword) for keyword in keywords}
        print("Лемматизированные ключевые слова:", lemmatized_keywords)

        for post in posts:
            # Лемматизируем текст поста
            matches = find_matches_in_text(post.text, lemmatized_keywords)
            if matches:
                print(f"Совпадения в посте {post.post_id}: {matches}")
            else:
                print(f"Нет совпадений в посте {post.post_id}")
