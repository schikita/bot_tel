from tortoise import Tortoise

DATABASE_HOST = "localhost"
DATABASE_PORT = 5432
DATABASE_USER = "postgres"
DATABASE_PASSWORD = ""
DATABASE_NAME = "db_bot_teleg"
TIMEZONE = "UTC"

DB_CONFIG = {
    "connections": {
        "default": {
            "engine": "tortoise.backends.asyncpg",
            "credentials": {
                "host": DATABASE_HOST,
                "port": 5432,
                "user": DATABASE_USER,
                "password": DATABASE_PASSWORD,
                "database": DATABASE_NAME,
                "schema": "public",
            },
        },
    },
    "apps": {
        "models": {
            "models": ["db.models"],
            "default_connection": "default",
        },
    },
    "timezone": TIMEZONE,
}


async def init_db():
    await Tortoise.init(config=DB_CONFIG)


async def close():
    await Tortoise.close_connections()
