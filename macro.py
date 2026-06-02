# macro.py — Full macro data using Yahoo Finance direct HTTP
import requests
import feedparser
import os
from datetime import datetime, timedelta

FRED_API_KEY = os.environ.get("FRED_API_KEY", "")
FRED_BASE    = "https://api.stlouisfed.org/fred/series/observations"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "application/json",
}

def fetch_yahoo_quote(symbol):
    """Fetch latest price and change for any Yahoo Finance symbol."""
    try:
        url  = f"https://query1.finance.yahoo.com/v8/finance/chart/{symbol}?range=5d&interval=1d"
        resp = requests.get(url, headers=HEADERS, timeout=10)
        if resp.status_code != 200:
            return None, None, None

        data   = resp.json()
        result = data.get("chart", {}).get("result", [])
        if not result:
            return None, None, None

        meta   = result[0].get("meta", {})
        closes = result[0].get("indicators", {}).get("quote", [{}])[0].get("close", [])
        closes = [c for c in closes if c is not None]

        if len(closes) >= 2:
            current = round(float(closes[-1]), 2)
            prev    = round(float(closes[-2]), 2)
            change  = round(((current - prev) / prev) * 100, 2)
            return current, prev, change
        elif len(closes) == 1:
            current = round(float(closes[-1]), 2)
            return current, current, 0.0

    except Exception as e:
        pass
    return None, None, None

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

def get_macro_environment():
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

    # ── VIX ──────────────────────────────────────────────────
    try:
        vix, vix_prev, vix_change = fetch_yahoo_quote("%5EVIX")
        if vix:
            macro["vix"] = {
                "value":  vix,
                "change": vix_change,
            }
            if vix < 15:
                macro["vix"]["signal"] = "✅ VIX LOW — Risk ON"
                bullish_count += 2
                macro["summary"].append(f"VIX {vix} — Very low fear, risk on")
            elif vix < 20:
                macro["vix"]["signal"] = "✅ VIX CALM — Mild risk on"
                bullish_count += 1
                macro["summary"].append(f"VIX {vix} — Calm market")
            elif vix < 30:
                macro["vix"]["signal"] = "⚠️ VIX ELEVATED — Caution"
                bearish_count += 1
                macro["summary"].append(f"VIX {vix} — Elevated fear")
            else:
                macro["vix"]["signal"] = "🔴 VIX HIGH — Risk OFF"
                bearish_count += 2
                macro["alerts"].append(f"⚠️ VIX SPIKE: {vix}")

            if vix_change and vix_change > 15:
                macro["alerts"].append(f"🚨 VIX SURGING +{vix_change}%")
            elif vix_change and vix_change < -10:
                macro["alerts"].append(f"✅ VIX FALLING {vix_change}%")
        else:
            macro["vix"] = {"value": "N/A", "signal": "Unavailable"}
    except Exception as e:
        macro["vix"] = {"value": "N/A", "signal": str(e)}

    # ── DXY ──────────────────────────────────────────────────
    try:
        dxy, dxy_prev, dxy_change = fetch_yahoo_quote("DX-Y.NYB")
        if dxy:
            macro["dxy"] = {
                "value":  dxy,
                "change": dxy_change,
            }
            if dxy_change and dxy_change < -0.3:
                macro["dxy"]["signal"] = "✅ DXY FALLING — Bullish for stocks & NSE"
                bullish_count += 1
                macro["summary"].append(f"DXY {dxy} falling — good for equities")
            elif dxy_change and dxy_change > 0.3:
                macro["dxy"]["signal"] = "⚠️ DXY RISING — Headwind for stocks"
                bearish_count += 1
                macro["summary"].append(f"DXY {dxy} rising — headwind")
            else:
                macro["dxy"]["signal"] = f"◆ DXY STABLE at {dxy}"
        else:
            macro["dxy"] = {"value": "N/A", "signal": "Unavailable"}
    except Exception as e:
        macro["dxy"] = {"value": "N/A", "signal": str(e)}

    # ── 10yr Bond Yield ───────────────────────────────────────
    try:
        tnx, tnx_prev, tnx_change = fetch_yahoo_quote("%5ETNX")
        if tnx:
            # TNX is quoted as percentage * 10
            yield_val    = round(tnx / 10, 3) if tnx > 10 else tnx
            yield_change = round(tnx_change, 3) if tnx_change else 0

            macro["bonds"] = {
                "yield_10yr": yield_val,
                "change":     yield_change,
            }
            if yield_change > 0.05:
                macro["bonds"]["signal"] = "⚠️ YIELDS RISING — Pressure on growth/tech"
                bearish_count += 1
                macro["summary"].append(f"10yr yield {yield_val}% rising")
            elif yield_change < -0.05:
                macro["bonds"]["signal"] = "✅ YIELDS FALLING — Bullish for tech"
                bullish_count += 1
                macro["summary"].append(f"10yr yield {yield_val}% falling")
            else:
                macro["bonds"]["signal"] = f"◆ Yields stable at {yield_val}%"
        else:
            macro["bonds"] = {"yield_10yr": "N/A", "signal": "Unavailable"}
    except Exception as e:
        macro["bonds"] = {"yield_10yr": "N/A", "signal": str(e)}

    # ── FRED: CPI + Fed Rate ──────────────────────────────────
    try:
        cpi, cpi_prev = get_fred_data("CPIAUCSL")
        if cpi and cpi_prev:
            cpi_change = ((cpi - cpi_prev) / cpi_prev) * 100
            macro["fred"]["cpi"] = {"value": round(cpi,2), "change": round(cpi_change,3)}
            if cpi_change > 0.3:
                bearish_count += 1
                macro["alerts"].append(f"🔴 CPI RISING {cpi:.2f} — Inflation up")
            elif cpi_change < -0.1:
                bullish_count += 1
                macro["alerts"].append(f"✅ CPI FALLING {cpi:.2f} — Fed may cut")
    except:
        pass

    try:
        fed, fed_prev = get_fred_data("FEDFUNDS")
        if fed:
            macro["fred"]["fed_rate"] = {"value": round(fed,2)}
            if fed > 5.0:
                bearish_count += 1
                macro["summary"].append(f"Fed Rate {fed:.2f}% — High")
            elif fed < 3.0:
                bullish_count += 1
                macro["summary"].append(f"Fed Rate {fed:.2f}% — Low, bullish")
    except:
        pass

    # ── Fed/CPI News ──────────────────────────────────────────
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
        macro["environment"]    = "RISK ON 🟢"
        macro["score_modifier"] = +1
    elif net >= 1:
        macro["environment"]    = "MILDLY BULLISH 🟡"
        macro["score_modifier"] = 0
    elif net <= -3:
        macro["environment"]    = "RISK OFF 🔴"
        macro["score_modifier"] = -1
    elif net <= -1:
        macro["environment"]    = "CAUTIOUS 🟠"
        macro["score_modifier"] = -1
    else:
        macro["environment"]    = "NEUTRAL ⚪"
        macro["score_modifier"] = 0

    return macro


def format_macro_alert(macro):
    env   = macro["environment"]
    vix   = macro.get("vix", {})
    dxy   = macro.get("dxy", {})
    bonds = macro.get("bonds", {})
    fred  = macro.get("fred", {})
    cpi   = fred.get("cpi", {})
    fed_r = fred.get("fed_rate", {})

    lines = [
        f"🌍 <b>MACRO: {env}</b>",
        "",
        f"😱 VIX: {vix.get('value','N/A')} ({vix.get('change',0):+.1f}%) — {vix.get('signal','')}",
        f"💵 DXY: {dxy.get('value','N/A')} ({dxy.get('change',0):+.2f}%) — {dxy.get('signal','')}",
        f"📉 10yr Yield: {bonds.get('yield_10yr','N/A')}% — {bonds.get('signal','')}",
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
