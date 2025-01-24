import asyncio
import logging

from src.config.settings import init_db
from src.services.parsers import ChannelParserService

channel_url = "https://t.me/s/sbbytoday"

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)



async def main():
    """Главная асинхронная функция."""
    await init_db()
    await ChannelParserService.parse_all_channels()

if __name__ == "__main__":
    asyncio.run(main())
