# trading/macro_calendar.py — Economic event risk scanner
# AI uses this to PREDICT macro risk, not just avoid it

import requests
import json
from datetime import datetime, timedelta, timezone

FRED_API_KEY = __import__('os').environ.get("FRED_API_KEY", "")

# High-impact events that move markets
HIGH_IMPACT_EVENTS = [
    "nonfarm payroll", "nfp", "jobs report", "employment situation",
    "fomc", "federal reserve", "interest rate decision", "fed meeting",
    "cpi", "inflation", "consumer price index",
    "pce", "personal consumption",
    "gdp", "gross domestic product",
    "ppi", "producer price",
    "ism manufacturing", "ism services",
    "retail sales", "consumer confidence",
    "jobless claims", "unemployment",
]

def get_macro_risk_score():
    """
    Assess current macro risk level using multiple data sources.
    Returns a risk score 0-10 and detailed context for the AI.
    """
    risk_score   = 0
    risk_factors = []
    bullish_factors = []
    context = {}

    try:
        # 1. Fed funds futures — what market expects for rates
        vix_data = _get_fred_series("VIXCLS")
        if vix_data:
            vix = float(vix_data)
            context["vix"] = vix
            if vix > 25:
                risk_score += 3
                risk_factors.append(f"VIX at {vix:.1f} — elevated fear, avoid new longs")
            elif vix > 20:
                risk_score += 1
                risk_factors.append(f"VIX at {vix:.1f} — moderate caution warranted")
            else:
                bullish_factors.append(f"VIX at {vix:.1f} — calm market, favours longs")

        # 2. 10-year yield — rate hike proxy
        yield_data = _get_fred_series("DGS10")
        if yield_data:
            y10 = float(yield_data)
            context["yield_10yr"] = y10
            if y10 > 4.8:
                risk_score += 3
                risk_factors.append(f"10yr yield at {y10:.2f}% — rate hike territory, tech headwind")
            elif y10 > 4.5:
                risk_score += 1
                risk_factors.append(f"10yr yield at {y10:.2f}% — elevated, watch growth stocks")
            else:
                bullish_factors.append(f"10yr yield at {y10:.2f}% — benign for equities")

        # 3. Yield curve — recession predictor
        yield_2yr = _get_fred_series("DGS2")
        if yield_2yr and yield_data:
            spread = float(yield_data) - float(yield_2yr)
            context["yield_curve"] = spread
            if spread < -0.5:
                risk_score += 2
                risk_factors.append(f"Yield curve inverted {spread:.2f}% — recession signal, be defensive")
            elif spread < 0:
                risk_score += 1
                risk_factors.append(f"Yield curve flat/inverted — caution on cyclicals")
            else:
                bullish_factors.append(f"Yield curve steepening {spread:.2f}% — economic expansion signal")

        # 4. Dollar strength — inverse to growth stocks
        dxy = _get_yahoo_price("DX-Y.NYB")
        if dxy:
            context["dxy"] = dxy
            if dxy > 105:
                risk_score += 2
                risk_factors.append(f"DXY at {dxy:.1f} — strong dollar headwind for growth/tech")
            elif dxy > 102:
                risk_score += 1
                risk_factors.append(f"DXY at {dxy:.1f} — watch dollar for headwinds")
            else:
                bullish_factors.append(f"DXY at {dxy:.1f} — weak dollar tailwind for growth")

        # 5. Credit spreads via HYG/LQD
        hyg = _get_yahoo_price("HYG")
        if hyg:
            context["hyg"] = hyg
            if hyg < 75:
                risk_score += 2
                risk_factors.append("HYG (junk bonds) weak — credit stress building, risk-off")
            elif hyg > 80:
                bullish_factors.append("HYG healthy — no credit stress, risk-on")

    except Exception as e:
        print(f"[MacroCalendar] Error: {e}")

    # Determine regime
    if risk_score >= 7:
        regime = "HIGH_RISK"
        recommendation = "DEFENSIVE: Hold cash, reduce position sizes to 5%, hedge with VXX"
    elif risk_score >= 4:
        regime = "ELEVATED_RISK"
        recommendation = "CAUTIOUS: Max 7% positions, prefer defensive sectors, avoid momentum chasing"
    elif risk_score >= 2:
        regime = "MODERATE"
        recommendation = "SELECTIVE: Normal position sizing, favour quality setups only"
    else:
        regime = "LOW_RISK"
        recommendation = "OPPORTUNISTIC: Full position sizing, momentum and growth plays viable"

    return {
        "risk_score":      risk_score,
        "regime":          regime,
        "recommendation":  recommendation,
        "risk_factors":    risk_factors,
        "bullish_factors": bullish_factors,
        "context":         context,
    }

def get_upcoming_events_risk():
    """
    Scan news for upcoming macro events to warn the AI.
    Instead of blocking trades, this gives probability context.
    """
    events = []
    try:
        import feedparser
        feeds = [
            "https://feeds.reuters.com/reuters/businessNews",
            "https://www.cnbc.com/id/100003114/device/rss/rss.html",
        ]
        for url in feeds:
            feed = feedparser.parse(url)
            for entry in feed.entries[:20]:
                title = entry.get("title", "").lower()
                for event in HIGH_IMPACT_EVENTS:
                    if event in title:
                        events.append({
                            "event":   entry.get("title", "")[:100],
                            "source":  "Reuters/CNBC",
                            "impact":  "HIGH",
                        })
                        break
    except:
        pass
    return events[:5]

def _get_fred_series(series_id):
    if not FRED_API_KEY:
        return None
    try:
        url = f"https://api.stlouisfed.org/fred/series/observations?series_id={series_id}&api_key={FRED_API_KEY}&file_type=json&limit=1&sort_order=desc"
        r = requests.get(url, timeout=8)
        if r.status_code == 200:
            obs = r.json().get("observations", [])
            if obs and obs[0]["value"] != ".":
                return obs[0]["value"]
    except:
        pass
    return None

def _get_yahoo_price(ticker):
    try:
        url = f"https://query1.finance.yahoo.com/v8/finance/chart/{ticker}?range=1d&interval=1d"
        r = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}, timeout=6)
        if r.status_code == 200:
            meta = r.json()["chart"]["result"][0]["meta"]
            return meta.get("regularMarketPrice") or meta.get("previousClose")
    except:
        pass
    return None
