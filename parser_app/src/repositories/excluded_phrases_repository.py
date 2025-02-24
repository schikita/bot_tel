from __future__ import annotations

from src.db.models import ExcludedPhrase

class ExcludedPhraseRepository:
    @staticmethod
    async def get_excluded_phrases() -> list[str]:
        return await ExcludedPhrase.all().values_list("phrase", flat=True)
