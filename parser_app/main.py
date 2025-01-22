import asyncio

from src.utils.http_requests import get_channel_posts
from src.utils.services import find_matches_in_text, get_keywords


async def parse_and_match(channel_url: str):
    """Получает посты с канала Telegram и ищет совпадения с ключевыми словами."""
    print(f"Получаем данные с канала: {channel_url}...")
    posts = await get_channel_posts(channel_url)

    if not posts:
        print("Не удалось получить данные с канала.")
        return

    print("Получаем ключевые слова из базы данных...")
    keywords = get_keywords()

    if not keywords:
        print("Нет ключевых слов для поиска.")
        return

    print("Ищем совпадения в постах...")
    for post in posts:
        matches = find_matches_in_text(post["text"], keywords)
        if matches:
            print(f"Post ID: {post['post_id']}")
            print(f"Совпадения: {', '.join(matches)}")
            print("-" * 50)

    print("Завершено.")


async def main():
    channel_url = "https://t.me/s/sbbytoday"  # Укажите URL канала
    await parse_and_match(channel_url)


if __name__ == "__main__":
    asyncio.run(main())
