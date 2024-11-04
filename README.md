# HN-bio-search

Hackernew Search by User Bio

A system that matches Hacker News stories with user interests based on their professional bio.

## Core Problem

Given a user's professional bio, find and rank the most relevant stories from Hacker News. This involves three key challenges:

1. Understanding user interests from unstructured text (bio)
2. Efficiently searching relevant HN stories
3. Ranking stories by relevance to user interests

## Design Thinking Process

### 1. Bio Analysis Strategy

Initially considered two approaches:

a) Simple keyword extraction
- Pros: Fast, straightforward
- Cons: Misses context, relationships between terms

b) Structured entity extraction (chosen approach)
- Pros:
  * Better understanding of user background
  * Separates different aspects (skills, interests, domain)
  * Allows weighted importance of different categories
- Cons: 
  * More complex
  * Requires good entity categorization

**Decision**: Chose structured approach because better understanding of bio leads to more relevant results.

### 2. Search Strategy

Considered approaches:

a) Fetch top N stories and filter (initial approach)
- Pros: Simple, comprehensive
- Cons: 
  * Limited by HN API rate limits
  * Many irrelevant stories to process
  * Misses older relevant stories

b) Multi-query targeted search (chosen approach)
- Pros:
  * More focused results
  * Can find older relevant stories
  * Better use of HN Search API capabilities
- Cons:
  * Multiple API calls needed
  * Need to handle duplicate results
  * Requires good query construction

**Decision**: Multi-query approach provides better coverage and relevance.

### 3. Ranking Strategy

Considered multiple approaches for merging and ranking results:

a) Score-based merge
- Pros: Mathematically sound
- Cons: 
  * Difficult to normalize scores across queries
  * May lead to topic concentration

b) Round robin selection (chosen approach)
- Pros:
  * Ensures diversity in results
  * Preserves relative ranking within each query
  * Simple to implement and maintain
  * Fair representation of different interest aspects
- Cons:
  * May not always reflect absolute relevance
  * Needs careful handling of duplicate stories

Implementation details:
- Each query result list maintains its internal ranking
- Stories are selected alternately from each list
- Batch processing (3 items per round) for efficiency
- Duplicate detection across result sets
- Weighted selection based on query importance

**Decision**: Round robin selection provides better topic diversity and interest coverage while maintaining reasonable relevance.

### Example Scenario

For a user bio: "Senior ML Engineer, interested in distributed systems and Rust programming"

Round robin selection would:
1. Create separate ranked lists for:
   - Machine Learning stories
   - Distributed Systems content
   - Rust-related posts
2. Pick top 3 stories from each category in rotation
3. Remove duplicates while preserving highest relevance position
4. Apply weights based on primary profession (ML) vs interests
## Implementation Architecture

```
User Bio → Bio Analysis → Concurrent Searches → Merge & Rank → Results
```

### Components

1. `BioAnalyzer`
   - Uses SpaCy for NLP
   - Categorizes entities into skills, tools, domains
   - Creates weighted search queries

2. `HNSearcher`
   - Handles Algolia API interaction
   - Concurrent searches for efficiency
   - Basic quality filtering

3. `RelevanceRanker`
   - TF-IDF vectorization
   - Cosine similarity computation
   - Multi-factor scoring

## Technical Decisions

1. **SpaCy over NLTK**
   - Better entity recognition
   - More modern API
   - Easier to extend

2. **Async Implementation**
   - Handles multiple searches efficiently
   - Better response times
   - Scales well with multiple users

3. **TF-IDF over Embeddings**
   - Simpler to implement and explain
   - Good enough for this use case
   - Faster computation
   - No need for large models

## Future Improvements

1. Refinements to Bio Analysis
   - Custom entity recognition for tech terms
   - Better categorization rules
   - User feedback incorporation

2. Search Optimization
   - Query optimization
   - Caching frequent searches
   - Rate limit handling

3. Ranking Enhancements
   - Time decay factor
   - User feedback learning
   - Domain-specific boosts

## Usage Example

```python
bio = """
I am a theoretical biologist, interested in disease ecology. 
My tools are R, clojure, compartmental disease modeling, 
and statistical GAM models.
"""

# Returns ranked list of relevant HN stories
results = await matcher.match_stories({"bio": bio})
```

## Performance Considerations

1. Caching
   - Bio analysis results
   - Common searches
   - Frequently requested stories

2. Concurrency
   - Parallel API calls
   - Async processing
   - Connection pooling

3. Resource Usage
   - Memory for caching
   - CPU for text processing
   - Network for API calls

## Error Handling

1. Bio Processing
   - Empty/invalid bios
   - Language detection
   - Entity extraction failures

2. HN API
   - Rate limits
   - API errors
   - Timeouts

3. Ranking
   - Missing data
   - Score normalization
   - Edge cases

This implementation prioritizes:
- Accuracy of matching
- Response time
- Code maintainability
- Scalability