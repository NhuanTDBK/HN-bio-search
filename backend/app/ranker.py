from typing import List
from app.models import SearchItemResponse


class RelevanceRanker:
    def __init__(self):
        pass

    def rank(self, query: str, stories: List[SearchItemResponse]):
        return sorted(
            stories,
            key=lambda x: (
                len(x._highlightResult.story_text.matchedWords)
                + len(x._highlightResult.title.matchedWords)
                if x._highlightResult
                else 0
            ),
            reverse=True,
        )
