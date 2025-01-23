import pymorphy3
from tortoise.exceptions import DoesNotExist

from src.db.models import SearchWord

morph = pymorphy3.MorphAnalyzer()


async def get_keywords():
    """Получаем ключевые слова из базы данных с использованием Tortoise ORM."""
    try:

        keywords = await SearchWord.all().values("word", "lemma")
        return keywords
    except DoesNotExist:
        return []


def lemmatize_text(text):
    """Лемматизация текста.
    Разделяет текст на слова и возвращает множество лемм.
    """
    words = text.split()
    return {morph.parse(word)[0].normal_form for word in words}


def find_matches_in_text(text, keywords):
    """Ищет совпадения ключевых слов в тексте."""
    lemmatized_text = lemmatize_text(text)
    return lemmatized_text.intersection(set(keywords))
