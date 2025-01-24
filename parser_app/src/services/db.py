
from src.services.lemma import lemmatize_word
from src.db.models import SearchWord


async def get_keywords() -> list[str]:
    """Получаем ключевые слова из базы данных с использованием Tortoise ORM."""
    keywords_data = await SearchWord.all().values("word", "lemma")
    return [
        keyword["lemma"] or lemmatize_word(keyword["word"])
        for keyword in keywords_data
    ]

