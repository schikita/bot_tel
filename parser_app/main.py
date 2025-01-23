import logging

from tortoise import Tortoise, run_async

from src.config.settings import DB_CONFIG
from src.utils.parsers import parse_and_match

channel_url = "https://t.me/s/sbbytoday"


logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


async def init_db():
    """Инициализация подключения к базе данных."""
    try:
        await Tortoise.init(config=DB_CONFIG)

        logger.info("Подключение к базе данных установлено успешно.")

    except Exception as e:
        logger.error(f"Ошибка подключения к базе данных: {e}")
        raise


async def main():
    await init_db()
    await parse_and_match(channel_url)


if __name__ == "__main__":
    run_async(main())
