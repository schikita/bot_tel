from tortoise import Tortoise   
import os

DATABASE_PORT = 5432
DATABASE_USER = os.environ.get("DB_USER", "postgres")
DATABASE_PASSWORD = os.environ.get("DB_PASSWORD", "")
DATABASE_NAME = os.environ.get("DB_NAME", "db_bot_teleg")
DATABASE_HOST = os.environ.get("DB_HOST", "localhost")
TIMEZONE = "UTC"
# 1869894953:AAG4YEXnaKWE7lSBgbecvRcBWIasyiY4o0U
TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN", "7809919634:AAF-vm4Cn8S75JdWZLE7mcQsLE25aDzchKU")


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
