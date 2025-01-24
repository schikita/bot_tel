from tortoise.exceptions import DoesNotExist

from src.db.models import SearchWord


async def get_keywords():
    """Получаем ключевые слова из базы данных с использованием Tortoise ORM."""
    try:

        keywords = await SearchWord.all().values("word", "lemma")
        return keywords
    except DoesNotExist:
        return []
