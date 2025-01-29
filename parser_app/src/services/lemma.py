from __future__ import annotations

from functools import lru_cache


class LemmaService:
    def __init__(self) -> None:
        pass

    @lru_cache(maxsize=10_000)
    def lemmatize_word(self, word: str) -> str:
        """Лемматизация слова (простейшая версия)."""
        return word.lower()

    def lemmatize_text(self, text: str) -> set[str]:
        """Лемматизация текста."""
        words = text.split()
        return {self.lemmatize_word(word) for word in words}

    def generate_phrases(self, text: str, n: int = 2) -> set[str]:
        """Генерация фраз (биграмм или триграмм) из текста."""
        words = text.split()
        phrases = set()

        for i in range(len(words) - n + 1):
            phrase = " ".join(words[i:i + n])
            phrases.add(phrase)

        return phrases

    def find_matches_in_text(self, text: str, keywords: set[str]) -> set[str]:
        """Ищет совпадения ключевых слов в тексте."""
        lemmatized_text = self.lemmatize_text(text)
        return lemmatized_text.intersection(keywords)


lemma_service = LemmaService()
