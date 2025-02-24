from __future__ import annotations

import re
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

    def remove_excluded_phrases(self, text: str, exclusions: list[str]) -> str:
        """Удаляет из текста заданные исключаемые фразы."""
        pattern = r"\b(?:" + "|".join(map(re.escape, exclusions)) + r")\b"
        cleaned_text = re.sub(pattern, "", text, flags=re.IGNORECASE).strip()

        # Убираем лишние пробелы и запятые, если они остались после удаления
        cleaned_text = re.sub(r"\s*,\s*", ", ", cleaned_text)
        cleaned_text = re.sub(r"\s+", " ", cleaned_text).strip()

        return cleaned_text

    def find_matches_in_text(
        self,
        text: str,
        keywords: set[str],
        *,
        lemmas: set[str] | None = None,
        excluded_phrases: list[str] | None = None,
    ) -> set[str]:
        """Ищет совпадения ключевых слов в тексте."""
        if excluded_phrases:
            text = self.remove_excluded_phrases(
                text,
                excluded_phrases
            )
        cleaned_text = self._remove_punctuation(text)
        lemmatized_text = self.lemmatize_text(cleaned_text)
        lemmatized_set = set(lemmatized_text)

        matches = set()

        raw_split = text.split()
        raw_split_lower = [w.lower() for w in raw_split]
        raw_set_lower = set(raw_split_lower)

        for keyword in keywords:
            keyword_words = keyword.split()
            if len(keyword_words) > 1:
                keyword_lemmas = [self.lemmatize_word(word) for word in keyword_words]
                for i in range(len(lemmatized_text) - len(keyword_lemmas) + 1):
                    if lemmatized_text[i : i + len(keyword_lemmas)] == keyword_lemmas:
                        matches.add(keyword)

            elif (
                keyword.lower() in lemmatized_set
                or self.lemmatize_word(keyword) in lemmatized_set
            ):
                matches.add(keyword)

            elif keyword.lower() in raw_set_lower:
                matches.add(keyword)

        if not lemmas:
            return matches

        for lemma in lemmas:
            lower_lemma = lemma.lower()
            if lower_lemma in lemmatized_set or lower_lemma in raw_set_lower:
                matches.add(lower_lemma)

        return matches

    def _remove_punctuation(self, text: str) -> str:
        """Удаляет всю пунктуацию (любые символы, не относящиеся к слову или пробелам)."""
        return re.sub(r"[^\w\s]+", "", text, flags=re.UNICODE)


morph = pymorphy3.MorphAnalyzer()
lemma_service = LemmaService(morph)
