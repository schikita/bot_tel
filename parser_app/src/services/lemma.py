from __future__ import annotations

from functools import lru_cache

import pymorphy3


class LemmaService:
    def __init__(self, morph: pymorphy3.MorphAnalyzer) -> None:
        self.morph = morph or pymorphy3.MorphAnalyzer()

    @lru_cache(maxsize=10_000)
    def lemmatize_word(self, word: str) -> str:
        """Лемматизация слова."""
        return self.morph.parse(word)[0].normal_form

    def lemmatize_text(self, text: str) -> list[str]:
        """Лемматизация текста.
        Разделяет текст на слова и возвращает множество лемм.
        """
        words = text.split()
        return [self.lemmatize_word(word) for word in words]

    def find_matches_in_text(self, text: str, keywords: set[str]) -> set[str]:
        """Ищет совпадения ключевых слов в тексте."""
        lemmatized_text = self.lemmatize_text(text)
        matches = set()

        for keyword in keywords:
            keyword_words = keyword.split()
            if len(keyword_words) > 1:
                keyword_lemmas = [self.lemmatize_word(word) for word in keyword_words]
                for i in range(len(lemmatized_text) - len(keyword_lemmas) + 1):
                    if lemmatized_text[i:i + len(keyword_lemmas)] == keyword_lemmas:
                        matches.add(keyword)
            elif keyword in lemmatized_text or self.lemmatize_word(keyword) in lemmatized_text:
                matches.add(keyword)

        return matches



morph = pymorphy3.MorphAnalyzer()
lemma_service = LemmaService(morph)
