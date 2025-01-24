import logging
import re
from typing import List, Optional

import httpx
from bs4 import BeautifulSoup

from src.schemas.posts import PostSchema

# Логирование
logger = logging.getLogger(__name__)

# Регулярные выражения для очистки текста
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


async def fetch_channel_data(url: str) -> Optional[str]:
    """Асинхронно получает HTML-код страницы канала с отключенной проверкой SSL-сертификатов."""
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36",
    }
    try:
        async with httpx.AsyncClient(
            headers=headers,
            verify=False,
            timeout=30,
        ) as client:
            response = await client.get(url)
            response.raise_for_status()
            return response.text
    except httpx.RequestError as e:
        logger.error(f"Ошибка при запросе {url}: {e}")
        return None


async def get_channel_posts(url: str) -> List[PostSchema]:
    """Получает список постов с Telegram-канала."""
    html = await fetch_channel_data(url)
    if html:
        posts = parse_posts_from_html(html)
        return posts
    return []


def parse_posts_from_html(html: str) -> List[PostSchema]:
    """Парсит HTML-код страницы канала и извлекает посты."""
    try:
        soup = BeautifulSoup(html, "html.parser")
        posts = []

        for post_div in soup.find_all("div", {"class": "tgme_widget_message"}):
            if not (post_id := extract_numeric_post_id(post_div.get("data-post", ""))):
                continue

            raw_text = _extract_raw_text(post_div)
            if cleaned_text := clean_text(raw_text) if raw_text else None:
                posts.append(PostSchema(post_id=post_id, text=cleaned_text))
        return posts

    except Exception as e:
        logger.error(f"Ошибка при парсинге HTML: {e}")
        return []


def _extract_raw_text(post_element) -> Optional[str]:
    """Извлекает сырой текст из элемента поста."""
    if text_container := post_element.find("div", class_="tgme_widget_message_bubble"):
        return text_container.get_text(strip=True)
    return None
