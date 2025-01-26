import asyncio
import logging

from src.config.settings import init_db
from src.services.parsers import ChannelParserService

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def main():
    """Главная асинхронная функция."""
    await init_db()
    while True:
        await ChannelParserService.parse_all_channels()
        await asyncio.sleep(5)


if __name__ == "__main__":
    asyncio.run(main())
