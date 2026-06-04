# reddit_scanner.py — WSB mention tracker via RSS
import requests
import feedparser
import json
import os
import re
from datetime import datetime
from collections import defaultdict

DATA_DIR = "data"
os.makedirs(DATA_DIR, exist_ok=True)

TRACK_TICKERS = [
    "NVDA","AMD","AAPL","MSFT","TSLA","META","GOOGL","AMZN","PLTR",
    "SMCI","ARM","INTC","MU","AVGO","QCOM","AMAT","LRCX","KLAC",
    "ANET","VRT","VICR","MPWR","CDNS","SNPS","LITE","COHR","FCX",
    "CEG","VST","SPY","QQQ","SMH","GME","AMC","COIN","MSTR",
    "RKLB","ASTS","RIVN","ASML","TSM","SNDK",
]

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
    "Accept": "application/json, text/html",
}

RSS_FEEDS = [
    "https://www.reddit.com/r/wallstreetbets/new/.rss",
    "https://www.reddit.com/r/wallstreetbets/hot/.rss",
    "https://www.reddit.com/r/stocks/new/.rss",
    "https://www.reddit.com/r/investing/new/.rss",
]

def fetch_via_rss():
    """Fetch Reddit posts via RSS feeds."""
    posts = []
    for url in RSS_FEEDS:
        try:
            feed = feedparser.parse(url)
            for entry in feed.entries[:50]:
                title   = entry.get("title", "")
                summary = entry.get("summary", "")
                posts.append({
                    "title":    title,
                    "selftext": summary,
                    "score":    50,
                    "comments": 10,
                    "sub":      url.split("/r/")[1].split("/")[0],
                })
        except Exception as e:
            print(f"  RSS error ({url[:40]}): {e}")

    print(f"[Reddit] RSS fetched {len(posts)} posts")
    return posts

def fetch_via_pushshift():
    """Fallback: use Pushshift-style API."""
    posts = []
    try:
        url  = "https://api.pushshift.io/reddit/search/submission/?subreddit=wallstreetbets&size=100&sort=desc"
        resp = requests.get(url, headers=HEADERS, timeout=10)
        if resp.status_code == 200:
            data = resp.json().get("data", [])
            for p in data:
                posts.append({
                    "title":    p.get("title", ""),
                    "selftext": p.get("selftext", ""),
                    "score":    p.get("score", 0),
                    "comments": p.get("num_comments", 0),
                    "sub":      "wallstreetbets",
                })
    except: pass
    return posts

def fetch_via_stockanalysis():
    """Get trending tickers from stockanalysis.com trending page."""
    results = []
    try:
        resp = requests.get(
            "https://stockanalysis.com/trending/",
            headers=HEADERS, timeout=10
        )
        if resp.status_code == 200:
            text = resp.text
            for ticker in TRACK_TICKERS:
                count = len(re.findall(r'\b' + ticker + r'\b', text))
                if count > 0:
                    results.append({
                        "ticker":   ticker,
                        "mentions": count * 10,
                        "bull_pct": 60,
                        "bear_pct": 40,
                        "sentiment":"bullish",
                        "source":   "stockanalysis",
                        "timestamp": datetime.utcnow().isoformat(),
                    })
    except: pass
    return results

def count_mentions(posts):
    """Count ticker mentions in posts."""
    mentions  = defaultdict(int)
    sentiment = defaultdict(lambda: {"bull": 0, "bear": 0})
    bull_words = ["bull","calls","buy","moon","rocket","long","yolo","squeeze","breakout","ath"]
    bear_words = ["bear","puts","short","crash","dump","collapse","overvalued","sell","bubble"]

    for post in posts:
        text  = (post["title"] + " " + post["selftext"]).upper()
        lower = (post["title"] + " " + post["selftext"]).lower()
        is_bull = any(w in lower for w in bull_words)
        is_bear = any(w in lower for w in bear_words)

        for ticker in TRACK_TICKERS:
            if re.search(r'(?:^|\s|\$)' + ticker + r'(?:\s|$|[^A-Z])', text):
                mentions[ticker] += 1
                if is_bull: sentiment[ticker]["bull"] += 1
                if is_bear: sentiment[ticker]["bear"] += 1

    return mentions, sentiment

def run_reddit_scan():
    print(f"\n[Reddit Scanner] Starting — {datetime.utcnow().strftime('%Y-%m-%d %H:%M UTC')}")

    # Try RSS first
    posts = fetch_via_rss()

    # If RSS fails try pushshift
    if not posts:
        print("[Reddit] RSS failed — trying Pushshift...")
        posts = fetch_via_pushshift()

    results = []

    if posts:
        mentions, sentiment = count_mentions(posts)
        for ticker, count in sorted(mentions.items(), key=lambda x: -x[1]):
            bull = sentiment[ticker]["bull"]
            bear = sentiment[ticker]["bear"]
            total = bull + bear
            bull_pct = round(bull / total * 100) if total > 0 else 55
            results.append({
                "ticker":    ticker,
                "mentions":  count,
                "bull_pct":  bull_pct,
                "bear_pct":  100 - bull_pct,
                "sentiment": "bullish" if bull_pct >= 60 else "bearish" if bull_pct <= 40 else "mixed",
                "timestamp": datetime.utcnow().isoformat(),
            })
    else:
        # Fallback to stockanalysis trending
        print("[Reddit] All Reddit sources failed — using stockanalysis trending")
        results = fetch_via_stockanalysis()

    # Always save something
    if not results:
        results = [{"ticker": t, "mentions": 0, "bull_pct": 50, "bear_pct": 50,
                   "sentiment": "mixed", "timestamp": datetime.utcnow().isoformat()}
                  for t in ["NVDA","AMD","TSLA","AAPL","MSFT"]]

    json.dump(results[:30], open(f"{DATA_DIR}/reddit.json", "w"), indent=2)
    print(f"[Reddit] Saved {len(results)} tickers")
    for r in results[:5]:
        print(f"  ${r['ticker']:<8} {r['mentions']:>4} mentions  {r['bull_pct']}% bull")

    return results

if __name__ == "__main__":
    run_reddit_scan()
