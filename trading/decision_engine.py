# trading/decision_engine.py
# Uses Claude AI to make intelligent buy/sell decisions
# based on all your trading rules

import json
import requests
import os
from datetime import datetime

ANTHROPIC_API_KEY = os.environ.get("ANTHROPIC_API_KEY", "")

TRADER_SYSTEM_PROMPT = """You are an elite quantitative trader managing a $183,000 paper trading portfolio.

YOUR TRADING RULES:
1. RSI: Buy when oversold (30-50). More timeframes oversold = stronger signal.
   Strongest swing: Daily + Weekly both oversold simultaneously.
2. Moving Averages: 200MA as key support/resistance. Golden Cross = strong bullish.
   Below 200MA + strong catalyst = short term trade using MA as resistance target.
3. Accumulation/Distribution: Rising A/D = institutions loading = buy confirmation.
4. Fibonacci: 61.8% retracement = golden ratio entry. 38.2% and 50% also valid.
5. Chart Patterns: Breakout with volume, FVG pullback, Support bounce.
6. News Catalyst: Trump mentions, government contracts, earnings beats OVERRIDE weak technicals.
7. Macro: VIX down = risk on. DXY down = bullish. Yields falling = buy tech/growth.
8. Bottleneck thesis: Own the supply chain constraints, not just the end product.

PORTFOLIO RULES:
- Max 10% per position
- Hard -7% stop loss on every position
- You decide profit taking based on conditions
- All trade types allowed: day trade, swing (days-weeks), position (months)
- Goal: Double the portfolio. Be aggressive but intelligent.

DECISION FRAMEWORK:
- Don't just look at score. Marry the catalyst + technicals + macro.
- A strong news catalyst (Trump, government contract, earnings beat) = buy even with weak technicals
- Bottleneck stocks: buy when the primary tech they serve is running
- When VIX is low and DXY is falling = deploy more capital aggressively
- Book profits when RSI is overbought on multiple timeframes OR news catalyst has played out
- Always write clear reasoning for every decision

You must respond ONLY with valid JSON. No markdown, no explanation outside JSON."""

def make_trading_decision(scan_results, portfolio, macro, current_prices):
    """
    Use Claude AI to make buy/sell decisions.
    Returns list of trade actions.
    """
    if not ANTHROPIC_API_KEY:
        print("[Trader] No ANTHROPIC_API_KEY — skipping AI decisions")
        return []

    # Build context for AI
    portfolio_summary = {
        "cash":        portfolio["cash"],
        "total_value": portfolio["total_value"],
        "pnl":         portfolio["pnl"],
        "pnl_pct":     portfolio["pnl_pct"],
        "positions":   {t: {
            "shares":       p["shares"],
            "entry_price":  p["entry_price"],
            "current_price":p.get("current_price", p["entry_price"]),
            "pnl_pct":      p.get("pnl_pct", 0),
            "trade_type":   p["trade_type"],
            "reasoning":    p["reasoning"][:100],
        } for t, p in portfolio["positions"].items()},
    }

    # Top opportunities from scanner
    opportunities = []
    for r in scan_results[:20]:
        if r.get("conviction") == "SKIP":
            continue
        ticker = r["ticker"]
        opportunities.append({
            "ticker":      ticker,
            "name":        r.get("name", ticker),
            "score":       r.get("score", 0),
            "rating":      r.get("buy_rating", ""),
            "price":       current_prices.get(ticker, 0),
            "ma_signal":   r.get("ma", {}).get("ma_signal", ""),
            "cross":       r.get("ma", {}).get("cross", ""),
            "patterns":    r.get("patterns", [])[:3],
            "signals":     r.get("signals", [])[:3],
            "news":        [n["title"][:80] for n in r.get("news_signals", [])[:2]],
            "rsi_daily":   r.get("rsi", {}).get("daily", {}).get("rsi"),
            "rsi_weekly":  r.get("rsi", {}).get("weekly", {}).get("rsi"),
        })

    macro_summary = {
        "environment": macro.get("environment", "NEUTRAL"),
        "vix":        macro.get("vix", {}).get("value", "N/A"),
        "dxy":        macro.get("dxy", {}).get("value", "N/A"),
        "yield_10yr": macro.get("bonds", {}).get("yield_10yr", "N/A"),
        "tlt_change": macro.get("bond_etfs", {}).get("TLT", {}).get("change", 0),
        "alerts":     macro.get("alerts", []),
    }

    prompt = f"""Current time: {datetime.utcnow().strftime('%Y-%m-%d %H:%M UTC')}

PORTFOLIO STATE:
{json.dumps(portfolio_summary, indent=2)}

MACRO ENVIRONMENT:
{json.dumps(macro_summary, indent=2)}

SCAN OPPORTUNITIES (top {len(opportunities)}):
{json.dumps(opportunities, indent=2)}

Based on all this data, make trading decisions. Apply all the trading rules.
Think about:
1. Which positions to SELL (stop loss hit, RSI overbought, catalyst played out, better opportunity)
2. Which stocks to BUY (best risk/reward, marry catalyst + technicals + macro)
3. Position sizing (max 10% per stock = max ${portfolio['total_value'] * 0.10:,.0f})

Return a JSON array of actions:
[
  {{
    "action": "BUY" or "SELL",
    "ticker": "NVDA",
    "trade_type": "day" or "swing" or "position",
    "reasoning": "Detailed reasoning (2-3 sentences explaining exactly why)",
    "confidence": "HIGH" or "MEDIUM" or "LOW",
    "hold_duration": "2-3 days" or "2-3 weeks" or "1-3 months",
    "target_pct": 15.0,
    "risk_note": "What would make you wrong on this trade"
  }}
]

Return [] if no good opportunities. Max 3 new buys per scan to avoid overtrading.
IMPORTANT: Only buy if you have genuine conviction. Quality over quantity."""

    try:
        resp = requests.post(
            "https://api.anthropic.com/v1/messages",
            headers={
                "x-api-key":         ANTHROPIC_API_KEY,
                "anthropic-version": "2023-06-01",
                "content-type":      "application/json",
            },
            json={
                "model":      "claude-sonnet-4-20250514",
                "max_tokens": 1500,
                "system":     TRADER_SYSTEM_PROMPT,
                "messages":   [{"role": "user", "content": prompt}],
            },
            timeout=30,
        )

        if resp.status_code != 200:
            print(f"[Trader] API error: {resp.status_code}")
            return []

        content = resp.json().get("content", [{}])[0].get("text", "[]")
        content = content.replace("```json", "").replace("```", "").strip()
        match   = __import__("re").search(r'\[[\s\S]*\]', content)
        if match:
            actions = json.loads(match.group(0))
            print(f"[Trader] AI decided {len(actions)} action(s)")
            return actions

    except Exception as e:
        print(f"[Trader] Decision error: {e}")

    return []
