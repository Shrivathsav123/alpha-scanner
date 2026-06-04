# reddit_scanner.py — Real WSB mention tracker
import requests
import feedparser
import json
import os
import re
from datetime import datetime, timezone, timedelta
from collections import defaultdict

DATA_DIR = "data"
os.makedirs(DATA_DIR, exist_ok=True)

# Tickers to track
TRACK_TICKERS = [
    "NVDA","AMD","AAPL","MSFT","TSLA","META","GOOGL","AMZN","PLTR",
    "SMCI","ARM","INTC","MU","SNDK","AVGO","QCOM","TSM","AMAT","LRCX",
    "ANET","VRT","VICR","MPWR","CDNS","SNPS","LITE","COHR","FCX",
    "CEG","VST","SPY","QQQ","SMH","SOXX","GME","AMC","COIN","HOOD",
    "RXRX","SOUN","IONQ","RGTI","QUBT","MSTR","IBIT","ABNB","UBER",
    "LYFT","RKLB","ASTS","LUNR","JOBY","ACHR","RIVN","LCID",
]

HEADERS = {
    "User-Agent": "AlphaTerminal/1.0 (market research tool)",
    "Accept": "application/json",
}

def fetch_wsb_posts():
    """Fetch latest WSB posts via Reddit RSS."""
    posts = []
    urls = [
        "https://www.reddit.com/r/wallstreetbets/new.json?limit=100",
        "https://www.reddit.com/r/wallstreetbets/hot.json?limit=50",
        "https://www.reddit.com/r/stocks/new.json?limit=50",
        "https://www.reddit.com/r/investing/new.json?limit=50",
        "https://www.reddit.com/r/options/new.json?limit=30",
    ]
    for url in urls:
        try:
            resp = requests.get(url, headers=HEADERS, timeout=10)
            if resp.status_code == 200:
                data = resp.json()
                children = data.get("data", {}).get("children", [])
                for child in children:
                    post = child.get("data", {})
                    posts.append({
                        "title":     post.get("title", ""),
                        "selftext":  post.get("selftext", ""),
                        "score":     post.get("score", 0),
                        "comments":  post.get("num_comments", 0),
                        "subreddit": post.get("subreddit", ""),
                        "created":   post.get("created_utc", 0),
                        "url":       post.get("url", ""),
                    })
        except Exception as e:
            print(f"  Reddit fetch error ({url[:40]}): {e}")

    print(f"[Reddit] Fetched {len(posts)} posts")
    return posts

def count_mentions(posts):
    """Count how many times each ticker is mentioned."""
    mentions     = defaultdict(int)
    sentiment    = defaultdict(lambda: {"bull": 0, "bear": 0})
    top_posts    = defaultdict(list)

    bull_words = ["bull", "calls", "buy", "moon", "rocket", "long", "yolo", "squeeze", "breakout", "ath", "pump"]
    bear_words = ["bear", "puts", "short", "crash", "dump", "collapse", "overvalued", "sell", "bubble"]

    # Only count recent posts (last 24 hours)
    cutoff = datetime.now(timezone.utc) - timedelta(hours=24)

    for post in posts:
        created = datetime.fromtimestamp(post.get("created", 0), tz=timezone.utc)
        if created < cutoff:
            continue

        text  = (post["title"] + " " + post["selftext"]).upper()
        lower = (post["title"] + " " + post["selftext"]).lower()
        score = post.get("score", 0)

        # Sentiment of post
        is_bull = any(w in lower for w in bull_words)
        is_bear = any(w in lower for w in bear_words)

        for ticker in TRACK_TICKERS:
            # Match $TICKER or standalone TICKER with word boundaries
            pattern = r'(?:^|\s|\$)' + ticker + r'(?:\s|$|[^A-Z])'
            if re.search(pattern, text):
                # Weight by engagement
                weight = 1 + min(score // 100, 5) + min(post.get("comments", 0) // 20, 3)
                mentions[ticker] += weight

                if is_bull: sentiment[ticker]["bull"] += 1
                if is_bear: sentiment[ticker]["bear"] += 1

                if len(top_posts[ticker]) < 3 and post["title"]:
                    top_posts[ticker].append({
                        "title":    post["title"][:100],
                        "score":    score,
                        "comments": post.get("comments", 0),
                        "sub":      post.get("subreddit", ""),
                    })

    return mentions, sentiment, top_posts

def run_reddit_scan():
    """Full Reddit scan — fetch, count, save."""
    print(f"\n[Reddit Scanner] Starting — {datetime.utcnow().strftime('%Y-%m-%d %H:%M UTC')}")

    posts = fetch_wsb_posts()
    if not posts:
        print("[Reddit] No posts fetched")
        return []

    mentions, sentiment, top_posts = count_mentions(posts)

    # Build results sorted by mentions
    results = []
    for ticker, count in sorted(mentions.items(), key=lambda x: -x[1]):
        if count == 0:
            continue
        bull = sentiment[ticker]["bull"]
        bear = sentiment[ticker]["bear"]
        total_sent = bull + bear
        bull_pct   = round(bull / total_sent * 100) if total_sent > 0 else 50

        results.append({
            "ticker":    ticker,
            "mentions":  count,
            "bull_pct":  bull_pct,
            "bear_pct":  100 - bull_pct,
            "sentiment": "bullish" if bull_pct >= 60 else "bearish" if bull_pct <= 40 else "mixed",
            "top_posts": top_posts.get(ticker, []),
            "timestamp": datetime.utcnow().isoformat(),
        })

    # Save to file
    json.dump(results[:30], open(f"{DATA_DIR}/reddit.json", "w"), indent=2)
    print(f"[Reddit] Saved {len(results)} tickers")

    # Print top 5
    for r in results[:5]:
        print(f"  ${r['ticker']:<8} {r['mentions']:>4} mentions  {r['bull_pct']}% bullish")

    return results

if __name__ == "__main__":
    run_reddit_scan()
