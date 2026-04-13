from fastapi import APIRouter, Query
from app.schemas.news import NewsResponse, NewsArticle
import feedparser
from datetime import datetime, timedelta
from typing import Optional
import hashlib
from functools import lru_cache
import time

router = APIRouter()

#RSS Feed Sources
RSS_FEEDS = [
    {"url": "https://www.autosport.com/rss/f1/news/", "source": "Autosport"},
    {"url": "https://www.motorsport.com/rss/f1/news/", "source": "Motorsport.com"},
    {"url": "https://www.the-race.com/feed/", "source": "The Race"}
]

# Fallback headlines (used when all feeds fail)
FALLBACK_HEADLINES = [
    {
        "id": "fallback-1",
        "title": "F1 Season Preview: Teams and Drivers Ready for Action",
        "blurb": "The new F1 season is underway with all teams fighting for championship glory.",
        "source": "F1 News",
        "url": "https://www.formula1.com",
        "published_at": datetime.now(),
        "category": "General",
        "image_url": None
    },
    {
        "id": "fallback-2",
        "title": "Technical Regulations: New Aero Updates This Season",
        "blurb": "FIA introduces new technical regulations affecting car performance.",
        "source": "F1 News",
        "url": "https://www.formula1.com",
        "published_at": datetime.now() - timedelta(hours=6),
        "category": "Technical",
        "image_url": None
    },
    {
        "id": "fallback-3",
        "title": "Driver Market: Latest Transfer Rumors and Confirmations",
        "blurb": "Stay updated with the latest driver moves and contract news.",
        "source": "F1 News",
        "url": "https://www.formula1.com",
        "published_at": datetime.now() - timedelta(hours=12),
        "category": "Drivers",
        "image_url": None
    },
    {
        "id": "fallback-4",
        "title": "Race Weekend Schedule: Upcoming Grands Prix",
        "blurb": "Check out the schedule for the next race weekend.",
        "source": "F1 News",
        "url": "https://www.formula1.com",
        "published_at": datetime.now() - timedelta(days=1),
        "category": "Schedule",
        "image_url": None
    },
    {
        "id": "fallback-5",
        "title": "Team Performance Analysis: Mid-Season Review",
        "blurb": "How are the teams performing so far this season?",
        "source": "F1 News",
        "url": "https://www.formula1.com",
        "published_at": datetime.now() - timedelta(days=2),
        "category": "Analysis",
        "image_url": None
    },
    {
        "id": "fallback-6",
        "title": "Championship Battle Heats Up",
        "blurb": "The fight for the championship is intensifying with every race.",
        "source": "F1 News",
        "url": "https://www.formula1.com",
        "published_at": datetime.now() - timedelta(days=3),
        "category": "Championship",
        "image_url": None
    }
]

#Cache storage (6 hour TTL)
_cache = {"data": None, "timestamp": None}
CACHE_TTL_SECONDS = 6 * 60 * 60  # 6 hours


def generate_article_id(title: str, url: str) -> str:
    """Generate unique ID from title and URL"""
    return hashlib.md5(f"{title}{url}".encode()).hexdigest()[:12]


def parse_feed(feed_url: str, source_name: str) -> list[NewsArticle]:
    """Parse a single RSS feed and return normalized articles"""
    articles = []
    
    try:
        feed = feedparser.parse(feed_url)
        
        for entry in feed.entries[:10]:  # Limit to 10 per feed
            # Parse publication date
            pub_date = datetime.now()
            if hasattr(entry, 'published_parsed') and entry.published_parsed:
                pub_date = datetime(*entry.published_parsed[:6])
            elif hasattr(entry, 'updated_parsed') and entry.updated_parsed:
                pub_date = datetime(*entry.updated_parsed[:6])

            image_url = None
            if hasattr(entry, 'media_content') and entry.media_content:
                image_url = entry.media_content[0].get('url')
            elif hasattr(entry, 'enclosures') and entry.enclosures:
                image_url = entry.enclosures[0].get('href')
            
            article = NewsArticle(
                id=generate_article_id(entry.title, entry.link),
                title=entry.title,
                blurb=entry.get('summary', '')[:200] if 'summary' in entry else None,
                source=source_name,
                url=entry.link,
                published_at=pub_date,
                category="F1 News",
                image_url=image_url
            )
            articles.append(article)
    
    except Exception as e:
        print(f"Error parsing feed {feed_url}: {e}")
    
    return articles


def fetch_all_feeds() -> list[NewsArticle]:
    """Fetch and parse all RSS feeds"""
    all_articles = []
    
    for feed_config in RSS_FEEDS:
        articles = parse_feed(feed_config["url"], feed_config["source"])
        all_articles.extend(articles)
    
    # Sort by publication date (newest first)
    all_articles.sort(key=lambda x: x.published_at, reverse=True)
    
    return all_articles


def get_cached_news() -> tuple[list[NewsArticle], bool]:
    """Get news from cache or fetch fresh"""
    global _cache
    
    if _cache["data"] and _cache["timestamp"]:
        age = time.time() - _cache["timestamp"]
        if age < CACHE_TTL_SECONDS:
            return _cache["data"], True
    
    #Cache expired or empty (fetch fresh data)
    try:
        articles = fetch_all_feeds()
        
        #If no articles fetched, use fallback
        if not articles:
            articles = [NewsArticle(**item) for item in FALLBACK_HEADLINES]

        _cache["data"] = articles
        _cache["timestamp"] = time.time()
        
        return articles, False
    
    except Exception as e:
        print(f"Error fetching feeds: {e}")
        return [NewsArticle(**item) for item in FALLBACK_HEADLINES], False


@router.get("", response_model=NewsResponse)
def get_news(race: Optional[str] = Query(None, description="Filter by race name")):
    """
    Get F1 news articles from RSS feeds

    """
    articles, cached = get_cached_news()
    
    if race:
        race_lower = race.lower()
        articles = [
            article for article in articles
            if race_lower in article.title.lower() or 
               (article.blurb and race_lower in article.blurb.lower())
        ]
    
    return NewsResponse(
        articles=articles,
        total=len(articles),
        cached=cached
    )