import asyncio

from src.utils.http_requests import get_channel_posts


async def main():
    channel_url = "https://t.me/s/sbbytoday"
    posts = await get_channel_posts(channel_url)

    if posts:
        for post in posts:
            print(f"Post ID: {post['post_id']}, Text: {post['text']}")
    else:
        print("Не удалось получить данные с канала.")


if __name__ == "__main__":
    asyncio.run(main())
