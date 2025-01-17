import asyncio

from tortoise import Tortoise


async def init():
    await Tortoise.init(
        db_url="postgres://username:password@localhost:5432/db_bot_teleg",
        modules={"models": ["parser_app.config.db.models"]},
    )


async def run():
    await init()
    print("Database connected and schemas generated.")


loop = asyncio.get_event_loop()
loop.run_until_complete(run())
