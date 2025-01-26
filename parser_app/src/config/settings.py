from tortoise import Tortoise

DATABASE_HOST = "localhost"
DATABASE_PORT = 5432
DATABASE_USER = "postgres"
DATABASE_PASSWORD = ""
DATABASE_NAME = "db_bot_teleg"
TIMEZONE = "UTC"

TELEGRAM_BOT_TOKEN = "1869894953:AAG4YEXnaKWE7lSBgbecvRcBWIasyiY4o0U"

DB_CONFIG = {
    "connections": {
        "default": {
            "engine": "tortoise.backends.asyncpg",
            "credentials": {
                "host": DATABASE_HOST,
                "port": DATABASE_PORT,
                "user": DATABASE_USER,
                "password": DATABASE_PASSWORD,
                "database": DATABASE_NAME,
                "schema": "public",
                "minsize": 10,
                "maxsize": 20,
                "max_queries": 100_000,
            },
        },
    },
    "apps": {
        "models": {
            "models": [
                "src.db.models",
            ],
            "default_connection": "default",
        },
    },
    "timezone": TIMEZONE,
}


async def init_db():
    """Инициализация подключения и генерация схем."""
    await Tortoise.init(config=DB_CONFIG)


async def close():
    """Закрытие подключения к базе данных."""
    await Tortoise.close_connections()
