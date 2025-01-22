import logging
import re

import httpx
from bs4 import BeautifulSoup

logger = logging.getLogger(__name__)


EMOJI_PATTERN = re.compile(
    r"[\U00010000-\U0010FFFF]|[\u2705\u274C\u26A1\u25B6\u2794\u267B\u2757]",
    flags=re.UNICODE,
)

UNWANTED_CONTENT_PATTERN = re.compile(
    r"Подписывайтесь@[\w]+|Please open Telegram to view this post|VIEW IN TELEGRAM|open Telegram to view this post|[\d]+views|[\d]{2}:[\d]{2}",
    flags=re.IGNORECASE,
)


def clean_text(text: str) -> str:
    """Убирает эмодзи, нежелательные строки и лишние пробелы из текста."""
    text = EMOJI_PATTERN.sub("", text)
    text = UNWANTED_CONTENT_PATTERN.sub("", text)
    return re.sub(r"\s+", " ", text).strip()


def extract_numeric_post_id(post_id: str) -> str:
    """Извлекает числовую часть Post ID."""
    match = re.search(r"/(\d+)$", post_id)
    return match.group(1) if match else post_id


def parse_posts_from_html(html: str):
    """Парсит HTML-код страницы канала и извлекает посты."""
    try:
        soup = BeautifulSoup(html, "html.parser")
        posts = []

        for post_div in soup.find_all("div", {"class": "tgme_widget_message"}):
            # Извлечение Post ID
            post_id_raw = post_div.get("data-post")
            post_id = extract_numeric_post_id(post_id_raw) if post_id_raw else None
            if not post_id:
                continue

            post_bubble = post_div.find("div", {"class": "tgme_widget_message_bubble"})
            if post_bubble:
                post_text = post_bubble.get_text(strip=True)
                cleaned_text = clean_text(post_text)

                if cleaned_text:
                    posts.append({"post_id": post_id, "text": cleaned_text})

        unique_posts = {post["post_id"]: post for post in posts}.values()
        return list(unique_posts)
    except Exception as e:
        logger.error(f"Ошибка при парсинге HTML: {e}")
        return []


async def fetch_channel_data(url: str):
    """Асинхронно получает HTML-код страницы канала."""
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36",
    }
    try:
        async with httpx.AsyncClient(headers=headers, verify=False) as client:
            response = await client.get(url)
            response.raise_for_status()
            return response.text
    except httpx.RequestError as e:
        logger.error(f"Ошибка при запросе {url}: {e}")
        return None


async def get_channel_posts(url: str):
    """Получает список постов с Telegram-канала."""
    html = await fetch_channel_data(url)
    if html:
        posts = parse_posts_from_html(html)
        return posts
    return []
