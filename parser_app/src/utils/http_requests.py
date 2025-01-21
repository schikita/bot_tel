import logging

import httpx
from bs4 import BeautifulSoup

logger = logging.getLogger(__name__)


async def fetch_channel_data(url: str):
    try:
        async with httpx.AsyncClient(verify=False) as client:
            response = await client.get(url)
            response.raise_for_status()
            return response.text
    except httpx.RequestError as e:
        logger.error(f"Ошибка при запросе {url}: {e}")
        return None


def parse_posts_from_html(html: str):
    try:
        soup = BeautifulSoup(html, "html.parser")
        posts = []

        for post_div in soup.find_all("div", {"class": "tgme_widget_message_bubble"}):
            post_text = post_div.get_text(strip=True)
            post_id = post_div.get("data-post")
            posts.append({"post_id": post_id, "text": post_text})

        return posts
    except Exception as e:
        logger.error(f"Ошибка при парсинге HTML: {e}")
        return []


async def get_channel_posts(url: str):
    html = await fetch_channel_data(url)
    if html:
        posts = parse_posts_from_html(html)
        return posts
    return []
