from fastapi import FastAPI
import asyncio
from gliner import GLiNER
from app.hn_searcher import HNSearcher
from app.models import SearchRequest
from app.ranker import RelevanceRanker

app = FastAPI()
model = GLiNER.from_pretrained("urchade/gliner_small-v1")
labels = [
    "Professional Background",
    "Area of Interest",
    "Education",
    "Skills",
]


@app.get("/")
async def read_root():
    return {"Hello": "World"}


@app.post("/search")
async def search(request: SearchRequest):
    hn_searcher = HNSearcher()
    entities = model.predict_entities(request.query, labels)

    entities_text = [entity["text"] for entity in entities]

    tasks = [
        hn_searcher.search_stories(query, hits_per_page=10) for query in entities_text
    ]
    agg_search_results = await asyncio.gather(*tasks)

    # Merge by interleaving results (first result from each query, then second, etc.), remove duplicates if any and return
    merged_results = []
    seen_results = set()
    ranker = RelevanceRanker()
    max_hits = max([res.nbHits for res in agg_search_results])
    total_hits = min(
        sum([res.nbHits for res in agg_search_results]), request.total_hits
    )
    nb_pages = total_hits // request.limit

    for i in range(max_hits):
        tmp_ranked = []
        for res in agg_search_results:
            if i < len(res.hits):
                if res.hits[i].objectID not in seen_results:
                    tmp_ranked.append(res.hits[i])
                    seen_results.add(res.hits[i].objectID)

        ranked = ranker.rank(request.query, tmp_ranked)
        merged_results.extend(ranked)

    resp = {
        "hits": merged_results,
        "page": request.page,
        "nbHits": total_hits,
        "nbPages": nb_pages,
    }

    return resp
