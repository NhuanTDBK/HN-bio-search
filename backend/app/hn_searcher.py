import httpx
from app.models import HNSearchResult


class HNSearcher:
    def __init__(self):
        self.base_url = "http://hn.algolia.com/api/v1"

    async def search_stories(
        self,
        query: str,
        hits_per_page: int = 100,
        page: int = 0,
        order_by: str = "relevance",
    ) -> HNSearchResult:
        """Search HN stories using Algolia API"""
        async with httpx.AsyncClient(follow_redirects=True) as client:
            search_url = (
                f"{self.base_url}/search"
                if order_by == "relevance"
                else f"{self.base_url}/search_by_date"
            )
            resp: httpx.Response = await client.get(
                search_url,
                params={
                    "query": query,
                    "tags": "story",
                    "hitsPerPage": hits_per_page,
                    "page": page,
                },
                headers={"Accept": "application/json"},
            )
            if not resp.is_success:
                resp.raise_for_status()

            return HNSearchResult.model_validate(resp.json())
