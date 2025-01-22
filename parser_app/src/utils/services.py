import pymorphy3

from src.db.models import SearchWord

morph = pymorphy3.MorphAnalyzer()


def get_keywords():
    """Получить ключевые слова из базы данных.
    Возвращается список лемматизированных ключевых слов.
    """
    return list(SearchWord.objects.values_list("lemma", flat=True))


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
