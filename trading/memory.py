# trading/memory.py — AI Trade Memory & Learning System
import json
import os
from datetime import datetime

DATA_DIR   = "data"
MEMORY_FILE = f"{DATA_DIR}/trade_memory.json"
LESSONS_FILE = f"{DATA_DIR}/lessons.json"

def load_memory():
    """Load all trade memories and lessons."""
    try:
        if os.path.exists(MEMORY_FILE):
            return json.load(open(MEMORY_FILE))
    except:
        pass
    return {
        "lessons":        [],
        "winning_setups": [],
        "losing_setups":  [],
        "stats":          {},
        "updated":        datetime.utcnow().isoformat(),
    }

def save_memory(memory):
    os.makedirs(DATA_DIR, exist_ok=True)
    memory["updated"] = datetime.utcnow().isoformat()
    json.dump(memory, open(MEMORY_FILE, "w"), indent=2, default=str)

def record_trade_outcome(trade, outcome_pct, held_days, macro_env):
    """
    Record what happened with a trade so AI can learn.
    Called when a position is closed.
    """
    memory = load_memory()
    won    = outcome_pct > 0

    # Build lesson
    lesson = {
        "date":       datetime.utcnow().isoformat(),
        "ticker":     trade.get("ticker", ""),
        "trade_type": trade.get("trade_type", "swing"),
        "entry":      trade.get("entry_price", 0),
        "exit":       trade.get("sell_price", 0),
        "pnl_pct":    outcome_pct,
        "held_days":  held_days,
        "won":        won,
        "reasoning":  trade.get("reasoning", ""),
        "macro":      macro_env,
        "lesson":     _generate_lesson(trade, outcome_pct, held_days),
    }

    memory["lessons"].insert(0, lesson)
    memory["lessons"] = memory["lessons"][:50]  # Keep last 50

    if won:
        memory["winning_setups"].insert(0, {
            "ticker":    trade.get("ticker"),
            "pnl_pct":  outcome_pct,
            "reasoning": trade.get("reasoning", "")[:150],
            "setup":     _extract_setup(trade.get("reasoning", "")),
        })
        memory["winning_setups"] = memory["winning_setups"][:20]
    else:
        memory["losing_setups"].insert(0, {
            "ticker":   trade.get("ticker"),
            "pnl_pct":  outcome_pct,
            "reasoning": trade.get("reasoning", "")[:150],
            "mistake":  _extract_mistake(trade.get("reasoning", ""), outcome_pct),
        })
        memory["losing_setups"] = memory["losing_setups"][:20]

    # Update stats
    all_trades   = memory["lessons"]
    wins         = [t for t in all_trades if t["won"]]
    losses       = [t for t in all_trades if not t["won"]]
    avg_win      = sum(t["pnl_pct"] for t in wins)  / len(wins)  if wins   else 0
    avg_loss     = sum(t["pnl_pct"] for t in losses) / len(losses) if losses else 0
    win_rate     = len(wins) / len(all_trades) * 100 if all_trades else 0
    profit_factor = abs(avg_win / avg_loss) if avg_loss != 0 else 0

    memory["stats"] = {
        "total_trades":   len(all_trades),
        "wins":           len(wins),
        "losses":         len(losses),
        "win_rate":       round(win_rate, 1),
        "avg_win_pct":    round(avg_win, 2),
        "avg_loss_pct":   round(avg_loss, 2),
        "profit_factor":  round(profit_factor, 2),
        "best_trade":     max((t["pnl_pct"] for t in all_trades), default=0),
        "worst_trade":    min((t["pnl_pct"] for t in all_trades), default=0),
    }

    save_memory(memory)
    return lesson

def _generate_lesson(trade, pnl_pct, held_days):
    """Generate a human-readable lesson from a trade outcome."""
    ticker    = trade.get("ticker", "")
    reasoning = trade.get("reasoning", "")
    won       = pnl_pct > 0

    if won:
        if pnl_pct > 10:
            return f"STRONG WIN on {ticker} (+{pnl_pct:.1f}% in {held_days}d). Setup worked perfectly. Repeat this pattern."
        else:
            return f"WIN on {ticker} (+{pnl_pct:.1f}% in {held_days}d). Thesis confirmed but modest gain."
    else:
        if pnl_pct < -7:
            return f"STOP LOSS on {ticker} ({pnl_pct:.1f}%). Stop loss system worked — limited the damage."
        elif "resistance" in reasoning.lower() and pnl_pct < 0:
            return f"LOSS on {ticker} ({pnl_pct:.1f}%). Bought near resistance — avoid entries at resistance levels next time."
        elif "overbought" in reasoning.lower():
            return f"LOSS on {ticker} ({pnl_pct:.1f}%). RSI was elevated. Don't buy overbought conditions."
        else:
            return f"LOSS on {ticker} ({pnl_pct:.1f}% in {held_days}d). Review the original thesis — what broke down?"

def _extract_setup(reasoning):
    """Extract the key setup from winning trade reasoning."""
    keywords = ["RSI oversold", "Golden Cross", "Fibonacci", "breakout", "support",
                "derived demand", "bottleneck", "Golden ratio", "divergence"]
    found = [k for k in keywords if k.lower() in reasoning.lower()]
    return " + ".join(found[:3]) if found else "technical setup"

def _extract_mistake(reasoning, pnl_pct):
    """Extract what went wrong in a losing trade."""
    if "resistance" in reasoning.lower():
        return "Entered near resistance — bought into selling pressure"
    elif pnl_pct < -5:
        return "Thesis broke down — stop loss correctly triggered"
    elif "macro" in reasoning.lower():
        return "Macro environment shifted against the trade"
    else:
        return "Entry timing was off — setup did not follow through"

def get_memory_context():
    """
    Get formatted memory context to inject into AI decision prompt.
    This is how the AI 'learns' — it reads its past lessons before deciding.
    """
    memory = load_memory()
    lessons  = memory.get("lessons", [])
    wins     = memory.get("winning_setups", [])
    losses   = memory.get("losing_setups", [])
    stats    = memory.get("stats", {})

    if not lessons:
        return "No trade history yet — this is your first set of trades."

    context = f"""
TRADE MEMORY & LESSONS LEARNED:

Performance Stats:
- Total trades: {stats.get('total_trades', 0)}
- Win rate: {stats.get('win_rate', 0)}%
- Avg win: +{stats.get('avg_win_pct', 0)}%
- Avg loss: {stats.get('avg_loss_pct', 0)}%
- Profit factor: {stats.get('profit_factor', 0)}x
- Best trade: +{stats.get('best_trade', 0)}%
- Worst trade: {stats.get('worst_trade', 0)}%

Recent Lessons (most recent first):
{chr(10).join([f"- {l['lesson']}" for l in lessons[:10]])}

What's Working (winning setups):
{chr(10).join([f"- {w['ticker']}: +{w['pnl_pct']:.1f}% — {w['setup']}" for w in wins[:5]])}

What's NOT Working (avoid these):
{chr(10).join([f"- {l['ticker']}: {l['pnl_pct']:.1f}% — {l['mistake']}" for l in losses[:5]])}

Apply these lessons to your current decisions. Repeat winning patterns. Avoid losing patterns.
"""
    return context.strip()
