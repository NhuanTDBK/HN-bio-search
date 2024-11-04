import json
from app.models import HNSearchResult
from app.ranker import get_ranker

sample = """
{"exhaustive":{"nbHits":false,"typo":false},"exhaustiveNbHits":false,"exhaustiveTypo":false,"hits":[{"_highlightResult":{"author":{"matchLevel":"none","matchedWords":[],"value":"anigbrowl"},"story_text":{"fullyHighlighted":false,"matchLevel":"full","matchedWords":["theoretical","biologist"],"value":"I want to map the dynamics of the blogosphere using URLs or keywords. I am familiar with tools for visualizing directed graphs like Gephi or Cytoscape. My problem is that I don't know how to harvest the data of how links spread through social media in the first place, so as to create the tables from which to build the directed graph.<p>For example, say PG writes an article on his blog. Of course it gets picked up on HN. Many other people then link to the HN discussion and/or the original article, in places like Reddit, StackExchange, GitHub, even Facebook. Other people in turn link to those secondary, tertiary, quaternary sources. If you could harvest a giant list of all the backlinks and dates thereof, you'd see the idea spread out from the original source, like when <em>biologists</em> splice in a gene for flourescence in order to track the population dynamics within a bacterial colony, or like epidemiological analyses.<p>Conversely, imagine scraping HN (and only HN) to measure depth, diversity, and dynamics of comment threads,  and following all story links back to their sources. Doing so would quickly reveal pg to be a major 'influencer' on HN without reading any of the content.<p>Can anyone suggests tools or services for acquisition of such datasets? ISTM that people in marketing or business development must already have such tools at their disposal. I've done a lot of searching on topics like 'network analysis of the blogosphere' and so on but almost invariably these lead back to <em>theoretical</em> papers or hand-curated datasets. I've built a few of those myself, but I really want to automate the process. Can anyone help?<p>tl;dr I want to map the interaction structures on social networks (comments, backlinks, etc.) to discover the most 'influential' nodes in a social graph without having to actually read everything."},"title":{"matchLevel":"none","matchedWords":[],"value":"Ask HN: How would I visualize URL propagation in the blogosphere?"}},"_tags":["story","author_anigbrowl","story_13133437","ask_hn"],"author":"anigbrowl","children":[13133593],"created_at":"2016-12-08T19:39:07Z","created_at_i":1481225947,"num_comments":0,"objectID":"13133437","points":1,"story_id":13133437,"story_text":"I want to map the dynamics of the blogosphere using URLs or keywords. I am familiar with tools for visualizing directed graphs like Gephi or Cytoscape. My problem is that I don&#x27;t know how to harvest the data of how links spread through social media in the first place, so as to create the tables from which to build the directed graph.<p>For example, say PG writes an article on his blog. Of course it gets picked up on HN. Many other people then link to the HN discussion and&#x2F;or the original article, in places like Reddit, StackExchange, GitHub, even Facebook. Other people in turn link to those secondary, tertiary, quaternary sources. If you could harvest a giant list of all the backlinks and dates thereof, you&#x27;d see the idea spread out from the original source, like when biologists splice in a gene for flourescence in order to track the population dynamics within a bacterial colony, or like epidemiological analyses.<p>Conversely, imagine scraping HN (and only HN) to measure depth, diversity, and dynamics of comment threads,  and following all story links back to their sources. Doing so would quickly reveal pg to be a major &#x27;influencer&#x27; on HN without reading any of the content.<p>Can anyone suggests tools or services for acquisition of such datasets? ISTM that people in marketing or business development must already have such tools at their disposal. I&#x27;ve done a lot of searching on topics like &#x27;network analysis of the blogosphere&#x27; and so on but almost invariably these lead back to theoretical papers or hand-curated datasets. I&#x27;ve built a few of those myself, but I really want to automate the process. Can anyone help?<p>tl;dr I want to map the interaction structures on social networks (comments, backlinks, etc.) to discover the most &#x27;influential&#x27; nodes in a social graph without having to actually read everything.","title":"Ask HN: How would I visualize URL propagation in the blogosphere?","updated_at":"2024-09-20T00:03:37Z"}],"hitsPerPage":2,"nbHits":1,"nbPages":1,"page":0,"params":"query=theoretical+biologist&tags=story&hitsPerPage=2&advancedSyntax=true&analyticsTags=backend","processingTimeMS":11,"processingTimingsMS":{"_request":{"roundTrip":13},"fetch":{"query":10,"total":10},"total":11},"query":"theoretical biologist","serverTimeMS":11}
"""

res = HNSearchResult.model_validate(json.loads(sample))
data = res.hits


# def test_relevance_ranker():
#     ranker = get_ranker("relevance")
#     ranked = ranker.rank("a", data)
#     assert len(ranked) == len(data)


def test_popularity_ranker():
    ranker = get_ranker("popular")
    ranked = ranker.rank("a", data)
    assert len(ranked) == len(data)


def test_date_ranker():
    ranker = get_ranker("date")
    ranked = ranker.rank("a", data)
    assert len(ranked) == len(data)
