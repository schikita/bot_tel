from typing import Set

import pymorphy3

morph = pymorphy3.MorphAnalyzer()


def lemmatize_word(word: str) -> str:
    """Лемматизация слова."""
    return morph.parse(word)[0].normal_form

def lemmatize_text(text: str) -> Set[str]:
    """Лемматизация текста.
    Разделяет текст на слова и возвращает множество лемм.
    """
    words = text.split()
    return {lemmatize_word(word) for word in words}


def find_matches_in_text(text: str, keywords: Set[str]) -> Set[str]:
    """Ищет совпадения ключевых слов в тексте."""
    lemmatized_text = lemmatize_text(text)
    return lemmatized_text.intersection(keywords)
