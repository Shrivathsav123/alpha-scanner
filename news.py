# news.py — Active news scanner across all major financial publications
import feedparser
import requests
import json
import os
import re
from datetime import datetime, timezone, timedelta

DATA_DIR = "data"
os.makedirs(DATA_DIR, exist_ok=True)

# ── Reputable financial news RSS feeds ──────────────────────────
GLOBAL_FEEDS = [
    # CNBC
    "https://www.cnbc.com/id/100003114/device/rss/rss.html",      # Markets
    "https://www.cnbc.com/id/10000664/device/rss/rss.html",       # Tech
    "https://www.cnbc.com/id/10001147/device/rss/rss.html",       # Health
    "https://www.cnbc.com/id/10000739/device/rss/rss.html",       # Energy
    # Reuters
    "https://feeds.reuters.com/reuters/businessNews",
    "https://feeds.reuters.com/reuters/technologyNews",
    "https://feeds.reuters.com/reuters/healthNews",
    # MarketWatch
    "https://feeds.marketwatch.com/marketwatch/topstories",
    "https://feeds.marketwatch.com/marketwatch/marketpulse",
    # Seeking Alpha
    "https://seekingalpha.com/feed.xml",
    # Yahoo Finance
    "https://finance.yahoo.com/news/rssindex",
    # Barrons
    "https://www.barrons.com/feed/rss/markets",
    # Investor's Business Daily
    "https://www.investors.com/feed/",
    # The Motley Fool
    "https://www.fool.com/feeds/index.aspx",
]

# Stock-specific Google News searches for each ticker
def get_ticker_feed_urls(ticker, company):
    """Generate RSS feed URLs specifically for this stock."""
    company_short = company.split()[0] if company else ticker
    return [
        f"https://news.google.com/rss/search?q={ticker}+stock&hl=en-US&gl=US&ceid=US:en",
        f"https://news.google.com/rss/search?q={ticker}+earnings+revenue+2026&hl=en-US&gl=US&ceid=US:en",
        f"https://news.google.com/rss/search?q={company_short}+contract+deal+partnership&hl=en-US&gl=US&ceid=US:en",
        f"https://news.google.com/rss/search?q={ticker}+upgrade+downgrade+analyst&hl=en-US&gl=US&ceid=US:en",
    ]

HIGH_IMPACT = [
    "earnings beat", "beats estimates", "beats expectations",
    "guidance raised", "raises guidance", "record revenue", "record profit",
    "trump", "executive order", "white house", "pentagon",
    "government contract", "awarded contract", "billion contract",
    "fda approved", "fda approval", "drug approved", "cleared by fda",
    "acquisition", "merger", "buyout", "takeover", "acquired by",
    "buyback", "share repurchase", "dividend increase",
    "upgrade", "buy rating", "overweight", "outperform", "target raised",
    "breakthrough", "clinical trial success", "phase 3",
    "strategic partnership", "joint venture", "licensing deal",
    "ai partnership", "data center", "hyperscaler",
    "opec", "oil production", "energy crisis",
    "rate cut", "fed pivot", "inflation data",
]

NEGATIVE_KEYWORDS = [
    "earnings miss", "misses estimates", "guidance cut", "lowers guidance",
    "fda rejected", "fda rejection", "clinical trial failed",
    "investigation", "sec probe", "fraud", "recall",
    "layoffs", "job cuts", "restructuring",
    "downgrade", "sell rating", "underperform", "target cut",
    "loses contract", "contract terminated",
]

def clean_html(text):
    """Remove HTML tags from text."""
    return re.sub(r'<[^>]+>', '', text or '').strip()

def fetch_feed(url, timeout=8):
    """Fetch and parse an RSS feed."""
    try:
        feed = feedparser.parse(url)
        return feed.entries[:20]
    except:
        return []

def score_article(title, summary=""):
    """Score an article by impact — positive or negative."""
    text  = (title + " " + summary).lower()
    score = 0
    for kw in HIGH_IMPACT:
        if kw in text:
            score += 2
    for kw in NEGATIVE_KEYWORDS:
        if kw in text:
            score -= 2
    return score

def is_recent(entry, hours=24):
    """Check if article is within last N hours."""
    try:
        import time
        published = entry.get("published_parsed") or entry.get("updated_parsed")
        if published:
            pub_time = datetime.fromtimestamp(time.mktime(published), tz=timezone.utc)
            cutoff   = datetime.now(timezone.utc) - timedelta(hours=hours)
            return pub_time > cutoff
    except:
        pass
    return True  # Include if we can't determine age

def get_stock_news(ticker, company="", max_articles=5):
    """
    Actively fetch news specifically about a stock from multiple sources.
    Returns scored, relevant articles.
    """
    articles = []
    seen_titles = set()

    # Fetch from stock-specific Google News feeds
    for url in get_ticker_feed_urls(ticker, company):
        entries = fetch_feed(url)
        for entry in entries:
            title   = clean_html(entry.get("title", ""))
            summary = clean_html(entry.get("summary", ""))
            link    = entry.get("link", "")

            if not title or title in seen_titles:
                continue

            # Make sure article is actually about this stock
            ticker_mentioned   = ticker.upper() in title.upper()
            company_mentioned  = company and company.split()[0].lower() in title.lower()

            if not ticker_mentioned and not company_mentioned:
                continue

            seen_titles.add(title)
            impact_score = score_article(title, summary)

            articles.append({
                "title":   title[:150],
                "summary": summary[:200] if summary else "",
                "link":    link,
                "source":  _extract_source(link, entry),
                "score":   impact_score,
                "recent":  is_recent(entry),
                "bull":    impact_score > 0,
                "bear":    impact_score < 0,
            })

    # Sort by impact score and recency
    articles.sort(key=lambda x: (x["recent"], x["score"]), reverse=True)
    return articles[:max_articles]

def _extract_source(url, entry):
    """Extract publication name from URL or feed."""
    source_map = {
        "cnbc.com":         "CNBC",
        "reuters.com":      "Reuters",
        "bloomberg.com":    "Bloomberg",
        "wsj.com":          "WSJ",
        "ft.com":           "FT",
        "marketwatch.com":  "MarketWatch",
        "seekingalpha.com": "Seeking Alpha",
        "fool.com":         "Motley Fool",
        "barrons.com":      "Barron's",
        "yahoo.com":        "Yahoo Finance",
        "investors.com":    "IBD",
        "businessinsider":  "Business Insider",
        "techcrunch.com":   "TechCrunch",
        "biopharmadive.com":"BioPharma Dive",
        "stat":             "STAT News",
    }
    url_lower = url.lower()
    for domain, name in source_map.items():
        if domain in url_lower:
            return name
    # Try feed source tag
    try:
        src = entry.get("source", {})
        if isinstance(src, dict):
            return src.get("title", "News")
    except:
        pass
    return "News"

def scan_global_news():
    """
    Continuously scan all major financial news sources.
    Returns all articles tagged to known tickers.
    """
    print(f"[News] Scanning global feeds...")
    all_articles = []
    seen = set()

    # Load known tickers for matching
    try:
        from universe import ALL_US
        known_tickers = list(ALL_US.keys())[:100]
    except:
        known_tickers = [
            "NVDA","AMD","AAPL","MSFT","GOOGL","AMZN","META","TSLA",
            "AMAT","LRCX","KLAC","ANET","VRT","VICR","CDNS","SNPS",
            "MRNA","BNTX","REGN","LLY","VRTX","GILD",
            "XOM","CVX","COP","OXY","HAL","SLB",
            "NOK","ERIC","INFN","CIEN","KTOS","RKLB",
            "FCX","SCCO","NEM","JPM","GS","V","MA",
        ]

    for feed_url in GLOBAL_FEEDS:
        entries = fetch_feed(feed_url)
        for entry in entries:
            title   = clean_html(entry.get("title",""))
            summary = clean_html(entry.get("summary",""))
            link    = entry.get("link","")

            if not title or title in seen:
                continue
            seen.add(title)

            # Find which tickers this article mentions
            text = (title + " " + summary).upper()
            mentioned = []
            for t in known_tickers:
                pattern = r'(?:^|\s|\$)' + t + r'(?:\s|$|[^A-Z])'
                if re.search(pattern, text):
                    mentioned.append(t)

            if not mentioned:
                continue

            impact = score_article(title, summary)

            all_articles.append({
                "title":    title[:150],
                "summary":  summary[:200],
                "link":     link,
                "source":   _extract_source(link, entry),
                "tickers":  mentioned[:5],
                "impact":   impact,
                "bull":     impact > 0,
                "bear":     impact < 0,
                "time":     datetime.utcnow().isoformat(),
                "recent":   is_recent(entry, hours=12),
            })

    # Sort by impact and recency
    all_articles.sort(key=lambda x: (x["recent"], abs(x["impact"])), reverse=True)
    print(f"[News] Found {len(all_articles)} tagged articles across {len(set(t for a in all_articles for t in a['tickers']))} tickers")
    return all_articles[:100]

def save_news_feed(articles):
    """Save news to file for the app to read."""
    json.dump(articles, open(f"{DATA_DIR}/news_feed.json","w"), indent=2)
    print(f"[News] Saved {len(articles)} articles to news_feed.json")

def get_news_for_scanner(ticker, company=""):
    """
    Called by the main scanner for each stock.
    Returns news signals with impact score.
    """
    articles = get_stock_news(ticker, company, max_articles=4)
    signals  = []
    score_add = 0

    for a in articles:
        if a["score"] > 0:
            signals.append({
                "title":  a["title"],
                "source": a["source"],
                "score":  a["score"],
                "bull":   True,
            })
            score_add += min(a["score"], 3)  # Max +3 from news
        elif a["score"] < 0:
            signals.append({
                "title":  a["title"],
                "source": a["source"],
                "score":  a["score"],
                "bear":   True,
            })
            score_add += max(a["score"], -2)  # Max -2 from negative news

    return signals, min(score_add, 3)  # Cap at +3 bonus

# ── Stock-specific news (for backward compat) ──────────────────
def get_stock_specific_news(ticker, company_name=""):
    articles, _ = get_news_for_scanner(ticker, company_name)
    return articles

if __name__ == "__main__":
    print("Testing news scanner...")
    # Test NOK
    articles = get_stock_news("NOK", "Nokia Corporation", max_articles=5)
    print(f"\nNOK — {len(articles)} articles:")
    for a in articles:
        print(f"  [{a['source']}] {a['title'][:80]} (score: {a['score']})")

    # Test global scan
    print("\nRunning global scan...")
    all_news = scan_global_news()
    print(f"Top 5 articles:")
    for a in all_news[:5]:
        print(f"  {a['tickers']} | [{a['source']}] {a['title'][:70]}")
