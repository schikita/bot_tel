from tortoise import Tortoise

DATABASE_HOST = "localhost"
DATABASE_PORT = 5432
DATABASE_USER = "ser"
DATABASE_PASSWORD = "1234"
DATABASE_NAME = "db_bot_teleg"
TIMEZONE = "UTC"

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
    await Tortoise.generate_schemas()


async def close():
    """Закрытие подключения к базе данных."""
    await Tortoise.close_connections()
