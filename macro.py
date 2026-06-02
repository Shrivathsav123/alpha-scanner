# macro.py — Macro environment using FRED + RSS feeds (no Yahoo Finance)
import requests
import feedparser
import os
from datetime import datetime, timedelta

FRED_API_KEY = os.environ.get("FRED_API_KEY", "")
FRED_BASE    = "https://api.stlouisfed.org/fred/series/observations"

def get_fred_data(series_id):
    """Fetch latest data from FRED API."""
    if not FRED_API_KEY:
        return None, None
    try:
        resp = requests.get(FRED_BASE, params={
            "series_id":  series_id,
            "api_key":    FRED_API_KEY,
            "file_type":  "json",
            "sort_order": "desc",
            "limit":      2,
        }, timeout=10)
        obs = resp.json().get("observations", [])
        if len(obs) >= 2:
            v1 = obs[0]["value"]
            v2 = obs[1]["value"]
            if v1 != "." and v2 != ".":
                return float(v1), float(v2)
    except:
        pass
    return None, None

def get_vix_from_cboe():
    """Get VIX from CBOE directly — no Yahoo needed."""
    try:
        url  = "https://cdn.cboe.com/api/global/delayed_quotes/charts/historical/_VIX.json"
        resp = requests.get(url, timeout=8)
        if resp.status_code == 200:
            data = resp.json()
            rows = data.get("data", [])
            if len(rows) >= 2:
                current = float(rows[-1][4])  # Close price
                prev    = float(rows[-2][4])
                return current, prev
    except:
        pass
    return None, None

def get_macro_environment():
    """
    Full macro environment scan.
    Sources: FRED API + CBOE + Google News RSS
    No Yahoo Finance — no rate limits!
    """
    macro = {
        "vix":           {},
        "dxy":           {},
        "bonds":         {},
        "fred":          {},
        "environment":   "NEUTRAL",
        "score_modifier": 0,
        "summary":       [],
        "alerts":        [],
        "fed_news":      [],
    }

    bullish_count = 0
    bearish_count = 0

    # ── VIX from CBOE ─────────────────────────────────────────
    try:
        vix_current, vix_prev = get_vix_from_cboe()

        if vix_current:
            vix_change = ((vix_current - vix_prev) / vix_prev * 100) if vix_prev else 0
            macro["vix"] = {
                "value":  round(vix_current, 2),
                "change": round(vix_change, 1),
            }

            if vix_current < 15:
                macro["vix"]["signal"] = "✅ VIX LOW — Risk ON"
                bullish_count += 2
                macro["summary"].append(f"VIX {vix_current:.1f} — Very low fear")
            elif vix_current < 20:
                macro["vix"]["signal"] = "✅ VIX CALM — Mild risk on"
                bullish_count += 1
                macro["summary"].append(f"VIX {vix_current:.1f} — Calm")
            elif vix_current < 30:
                macro["vix"]["signal"] = "⚠️ VIX ELEVATED — Caution"
                bearish_count += 1
                macro["summary"].append(f"VIX {vix_current:.1f} — Elevated fear")
            else:
                macro["vix"]["signal"] = "🔴 VIX HIGH — Risk OFF"
                bearish_count += 2
                macro["alerts"].append(f"⚠️ VIX SPIKE: {vix_current:.1f}")

            if vix_change > 15:
                macro["alerts"].append(f"🚨 VIX SURGING +{vix_change:.1f}%")
            elif vix_change < -10:
                macro["alerts"].append(f"✅ VIX FALLING {vix_change:.1f}%")
        else:
            macro["vix"] = {"value": "N/A", "signal": "VIX data unavailable"}

    except Exception as e:
        macro["vix"] = {"error": str(e)}

    # ── FRED: CPI Inflation ───────────────────────────────────
    try:
        cpi, cpi_prev = get_fred_data("CPIAUCSL")
        if cpi and cpi_prev:
            cpi_change = ((cpi - cpi_prev) / cpi_prev) * 100
            macro["fred"]["cpi"] = {
                "value":  round(cpi, 2),
                "change": round(cpi_change, 3),
            }
            if cpi_change > 0.3:
                bearish_count += 1
                macro["alerts"].append(f"🔴 CPI RISING: {cpi:.2f} (+{cpi_change:.2f}%) — Inflation up")
                macro["summary"].append(f"CPI {cpi:.2f} rising — inflation concern")
            elif cpi_change < -0.1:
                bullish_count += 1
                macro["alerts"].append(f"✅ CPI FALLING: {cpi:.2f} — Fed may cut")
                macro["summary"].append(f"CPI {cpi:.2f} falling — bullish")
    except:
        pass

    # ── FRED: Fed Funds Rate ──────────────────────────────────
    try:
        fed, fed_prev = get_fred_data("FEDFUNDS")
        if fed:
            macro["fred"]["fed_rate"] = {
                "value":  round(fed, 2),
                "change": round(fed - (fed_prev or fed), 2),
            }
            if fed > 5.0:
                bearish_count += 1
                macro["summary"].append(f"Fed Rate {fed:.2f}% — High, headwind")
            elif fed < 3.0:
                bullish_count += 1
                macro["summary"].append(f"Fed Rate {fed:.2f}% — Low, bullish")
    except:
        pass

    # ── FRED: 10yr Treasury Yield ─────────────────────────────
    try:
        t10, t10_prev = get_fred_data("DGS10")
        if t10:
            yield_change = t10 - (t10_prev or t10)
            macro["bonds"] = {
                "yield_10yr": round(t10, 3),
                "change":     round(yield_change, 3),
            }
            if yield_change > 0.05:
                bearish_count += 1
                macro["bonds"]["signal"] = "⚠️ YIELDS RISING — Pressure on growth"
                macro["summary"].append(f"10yr yield {t10:.2f}% rising")
            elif yield_change < -0.05:
                bullish_count += 1
                macro["bonds"]["signal"] = "✅ YIELDS FALLING — Bullish for tech"
                macro["summary"].append(f"10yr yield {t10:.2f}% falling")
            else:
                macro["bonds"]["signal"] = f"◆ Yields stable at {t10:.2f}%"
    except:
        pass

    # ── Fed/CPI News from Google RSS ──────────────────────────
    try:
        url  = "https://news.google.com/rss/search?q=Federal+Reserve+CPI+inflation+interest+rate+2026&hl=en-US&gl=US&ceid=US:en"
        feed = feedparser.parse(url)
        for entry in feed.entries[:5]:
            title = entry.get("title", "").lower()
            if any(w in title for w in ["cpi", "inflation", "fed", "rate", "powell", "fomc"]):
                macro["fed_news"].append(entry.get("title", ""))
                if any(w in title for w in ["rate cut", "dovish", "pause", "lower inflation"]):
                    bullish_count += 1
                elif any(w in title for w in ["rate hike", "hawkish", "higher inflation", "hot cpi"]):
                    bearish_count += 1
    except:
        pass

    # ── Overall Environment ───────────────────────────────────
    net = bullish_count - bearish_count
    if net >= 3:
        macro["environment"]     = "RISK ON 🟢"
        macro["score_modifier"]  = +1
    elif net >= 1:
        macro["environment"]     = "MILDLY BULLISH 🟡"
        macro["score_modifier"]  = 0
    elif net <= -3:
        macro["environment"]     = "RISK OFF 🔴"
        macro["score_modifier"]  = -1
    elif net <= -1:
        macro["environment"]     = "CAUTIOUS 🟠"
        macro["score_modifier"]  = -1
    else:
        macro["environment"]     = "NEUTRAL ⚪"
        macro["score_modifier"]  = 0

    return macro


def format_macro_alert(macro):
    """Format macro environment for Telegram."""
    env   = macro["environment"]
    vix   = macro.get("vix", {})
    bonds = macro.get("bonds", {})
    fred  = macro.get("fred", {})
    cpi   = fred.get("cpi", {})
    fed_r = fred.get("fed_rate", {})

    lines = [
        f"🌍 <b>MACRO: {env}</b>",
        "",
        f"😱 VIX: {vix.get('value','?')} — {vix.get('signal','')}",
        f"📉 10yr Yield: {bonds.get('yield_10yr','?')}% — {bonds.get('signal','')}",
    ]

    if cpi.get("value"):
        lines.append(f"📊 CPI: {cpi['value']} ({cpi.get('change',0):+.3f}%)")
    if fed_r.get("value"):
        lines.append(f"🏦 Fed Rate: {fed_r['value']}%")

    if macro.get("fed_news"):
        lines.append("")
        lines.append("📰 <b>Fed/CPI News:</b>")
        for n in macro["fed_news"][:2]:
            lines.append(f"• {n[:80]}")

    if macro.get("alerts"):
        lines.append("")
        lines.append("🚨 <b>Macro Alerts:</b>")
        for a in macro["alerts"]:
            lines.append(f"• {a}")

    return "\n".join(lines)
