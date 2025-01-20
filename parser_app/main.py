import asyncio

from src.config.settings import close, init_db


async def main():
    await init_db()

    await close()


if __name__ == "__main__":
    asyncio.run(main())
