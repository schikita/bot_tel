from src.utils.http_requests import get_channel_posts
from src.utils.services import find_matches_in_text, get_keywords


async def parse_and_match(channel_url):
    """Парсит новости с Telegram-канала и ищет совпадения с ключевыми словами."""
    # Получаем ключевые слова из базы данных
    keywords = get_keywords()
    if not keywords:
        print("Ключевые слова не заданы!")
        return

    # Парсим новости с Telegram-канала
    posts = await get_channel_posts(channel_url)
    if not posts:
        print("Не удалось получить данные с канала.")
        return

    # Поиск совпадений в новостях
    for post in posts:
        matches = find_matches_in_text(post["text"], keywords)
        if matches:
            print(f"Совпадения в посте {post['post_id']}: {', '.join(matches)}")
        else:
            print(f"Совпадений не найдено в посте {post['post_id']}")
