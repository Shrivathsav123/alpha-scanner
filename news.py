# news.py — Active news scanner across all major financial publications
import feedparser
import requests
import json
import os
import re
from datetime import datetime, timezone, timedelta

DATA_DIR = "data"
os.makedirs(DATA_DIR, exist_ok=True)

GLOBAL_FEEDS = [
    "https://www.cnbc.com/id/100003114/device/rss/rss.html",
    "https://www.cnbc.com/id/10000664/device/rss/rss.html",
    "https://www.cnbc.com/id/10001147/device/rss/rss.html",
    "https://www.cnbc.com/id/10000739/device/rss/rss.html",
    "https://feeds.reuters.com/reuters/businessNews",
    "https://feeds.reuters.com/reuters/technologyNews",
    "https://feeds.reuters.com/reuters/healthNews",
    "https://feeds.marketwatch.com/marketwatch/topstories",
    "https://feeds.marketwatch.com/marketwatch/marketpulse",
    "https://finance.yahoo.com/news/rssindex",
    "https://www.investors.com/feed/",
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
    return re.sub(r'<[^>]+>', '', text or '').strip()

def fetch_feed(url, timeout=8):
    try:
        feed = feedparser.parse(url)
        return feed.entries[:20]
    except:
        return []

def score_article(title, summary=""):
    text = (title + " " + summary).lower()
    score = 0
    for kw in HIGH_IMPACT:
        if kw in text:
            score += 2
    for kw in NEGATIVE_KEYWORDS:
        if kw in text:
            score -= 2
    return score

def is_recent(entry, hours=24):
    try:
        import time
        published = entry.get("published_parsed") or entry.get("updated_parsed")
        if published:
            pub_time = datetime.fromtimestamp(time.mktime(published), tz=timezone.utc)
            cutoff = datetime.now(timezone.utc) - timedelta(hours=hours)
            return pub_time > cutoff
    except:
        pass
    return True

def _extract_source(url, entry):
    source_map = {
        "cnbc.com": "CNBC",
        "reuters.com": "Reuters",
        "bloomberg.com": "Bloomberg",
        "wsj.com": "WSJ",
        "ft.com": "FT",
        "marketwatch.com": "MarketWatch",
        "seekingalpha.com": "Seeking Alpha",
        "fool.com": "Motley Fool",
        "barrons.com": "Barrons",
        "yahoo.com": "Yahoo Finance",
        "investors.com": "IBD",
        "biopharmadive.com": "BioPharma Dive",
    }
    url_lower = url.lower()
    for domain, name in source_map.items():
        if domain in url_lower:
            return name
    return "News"

def get_stock_news(ticker, company="", max_articles=5):
    articles = []
    seen_titles = set()
    queries = [
        f"{ticker}+stock+2026",
        f"{ticker}+earnings+revenue+guidance",
        f"{ticker}+contract+deal+partnership",
        f"{ticker}+analyst+upgrade+target",
    ]
    for q in queries[:3]:
        try:
            url = f"https://news.google.com/rss/search?q={q}&hl=en-US&gl=US&ceid=US:en"
            entries = fetch_feed(url)
            for entry in entries:
                title = clean_html(entry.get("title", ""))
                summary = clean_html(entry.get("summary", ""))
                link = entry.get("link", "")
                if not title or title in seen_titles:
                    continue
                ticker_mentioned = ticker.upper() in title.upper()
                company_mentioned = company and company.split()[0].lower() in title.lower()
                if not ticker_mentioned and not company_mentioned:
                    continue
                seen_titles.add(title)
                impact_score = score_article(title, summary)
                articles.append({
                    "title": title[:150],
                    "summary": summary[:200],
                    "link": link,
                    "source": _extract_source(link, entry),
                    "score": impact_score,
                    "recent": is_recent(entry),
                    "bull": impact_score > 0,
                    "bear": impact_score < 0,
                })
        except:
            pass
    articles.sort(key=lambda x: (x["recent"], x["score"]), reverse=True)
    return articles[:max_articles]

def scan_global_news():
    print("[News] Scanning global feeds...")
    all_articles = []
    seen = set()
    known_tickers = [
        "NVDA","AMD","AAPL","MSFT","GOOGL","AMZN","META","TSLA",
        "AMAT","LRCX","KLAC","ANET","VRT","VICR","CDNS","SNPS",
        "MRNA","BNTX","REGN","LLY","VRTX","GILD",
        "XOM","CVX","COP","OXY","HAL","SLB",
        "NOK","ERIC","INFN","CIEN","KTOS","RKLB",
        "FCX","SCCO","NEM","JPM","GS","V","MA",
        "MU","SNDK","AVGO","ASML","LRCX","KLAC",
    ]
    for feed_url in GLOBAL_FEEDS:
        entries = fetch_feed(feed_url)
        for entry in entries:
            title = clean_html(entry.get("title", ""))
            summary = clean_html(entry.get("summary", ""))
            link = entry.get("link", "")
            if not title or title in seen:
                continue
            seen.add(title)
            text = (title + " " + summary).upper()
            mentioned = []
            for t in known_tickers:
                if re.search(r'(?:^|\s|\$)' + t + r'(?:\s|$|[^A-Z])', text):
                    mentioned.append(t)
            if not mentioned:
                continue
            impact = score_article(title, summary)
            all_articles.append({
                "title": title[:150],
                "summary": summary[:200],
                "link": link,
                "source": _extract_source(link, entry),
                "tickers": mentioned[:5],
                "impact": impact,
                "bull": impact > 0,
                "bear": impact < 0,
                "time": datetime.utcnow().isoformat(),
                "recent": is_recent(entry, hours=12),
            })
    all_articles.sort(key=lambda x: (x["recent"], abs(x["impact"])), reverse=True)
    print(f"[News] Found {len(all_articles)} articles")
    return all_articles[:100]

def save_news_feed(articles):
    json.dump(articles, open(f"{DATA_DIR}/news_feed.json", "w"), indent=2)
    print(f"[News] Saved {len(articles)} articles")

def get_news_for_scanner(ticker, company=""):
    articles = get_stock_news(ticker, company, max_articles=4)
    signals = []
    score_add = 0
    for a in articles:
        if a["score"] > 0:
            signals.append({
                "title": a["title"],
                "source": a["source"],
                "score": a["score"],
                "bull": True,
            })
            score_add += min(a["score"], 3)
        elif a["score"] < 0:
            signals.append({
                "title": a["title"],
                "source": a["source"],
                "score": a["score"],
                "bear": True,
            })
            score_add += max(a["score"], -2)
    return signals, min(score_add, 3)

def scan_news_for_ticker(ticker, company=""):
    signals, score = get_news_for_scanner(ticker, company)
    return signals
