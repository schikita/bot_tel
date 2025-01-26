from __future__ import annotations

from src.db.models import SearchWord
from src.services.lemma import lemma_service


class SearchWordService:
    @staticmethod
    async def get_keywords() -> list[SearchWord]:
        """Получаем ключевые слова из базы данных"""
        return await SearchWord.all()

    @staticmethod
    async def get_lemmatized_keywords() -> set[str]:
        """Получаем лемматизированные ключевые слова из базы данных."""
        keywords_data = await SearchWord.all()
        return {
            keyword.lemma or lemma_service.lemmatize_word(keyword.word)
            for keyword in keywords_data
        }

    @staticmethod
    async def get_keywords_dict() -> dict[str, str]:
        """Получаем словарь с ключевыми словами и их леммами."""
        keywords = await SearchWord.all()
        return {keyword.word: keyword.lemma for keyword in keywords}

    @staticmethod
    async def fill_lemma_if_empty(search_word: SearchWord) -> SearchWord:
        if not search_word.lemma:
            search_word.lemma = lemma_service.lemmatize_word(search_word.word)
            await search_word.save()
        return search_word

    @staticmethod
    async def get_lemma(word: str) -> str:
        return lemma_service.lemmatize_word(word)
