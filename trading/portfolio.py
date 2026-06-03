# trading/portfolio.py — Paper trading portfolio manager
import json
import os
from datetime import datetime

DATA_DIR      = "data"
PORTFOLIO_FILE = f"{DATA_DIR}/portfolio.json"
TRADES_FILE    = f"{DATA_DIR}/trades.json"

STARTING_BALANCE = 183000.00
MAX_POSITION_PCT  = 0.10  # 10% max per stock
STOP_LOSS_PCT     = -0.07  # -7% hard stop

def load_portfolio():
    """Load portfolio state or create fresh one."""
    os.makedirs(DATA_DIR, exist_ok=True)
    try:
        if os.path.exists(PORTFOLIO_FILE):
            return json.load(open(PORTFOLIO_FILE))
    except:
        pass

    # Fresh portfolio
    portfolio = {
        "balance":      STARTING_BALANCE,
        "cash":         STARTING_BALANCE,
        "positions":    {},
        "total_value":  STARTING_BALANCE,
        "pnl":          0.0,
        "pnl_pct":      0.0,
        "created":      datetime.utcnow().isoformat(),
        "updated":      datetime.utcnow().isoformat(),
        "trades_count": 0,
        "wins":         0,
        "losses":       0,
    }
    save_portfolio(portfolio)
    return portfolio

def save_portfolio(portfolio):
    """Save portfolio state to file."""
    os.makedirs(DATA_DIR, exist_ok=True)
    portfolio["updated"] = datetime.utcnow().isoformat()
    json.dump(portfolio, open(PORTFOLIO_FILE, "w"), indent=2, default=str)

def load_trades():
    """Load trade history."""
    try:
        if os.path.exists(TRADES_FILE):
            return json.load(open(TRADES_FILE))
    except:
        pass
    return []

def save_trades(trades):
    """Save trade history (last 200)."""
    json.dump(trades[:200], open(TRADES_FILE, "w"), indent=2, default=str)

def update_position_prices(portfolio, current_prices):
    """Update all open positions with current market prices."""
    total_positions_value = 0

    for ticker, pos in portfolio["positions"].items():
        price = current_prices.get(ticker)
        if price:
            pos["current_price"] = price
            pos["value"]         = round(price * pos["shares"], 2)
            pos["pnl"]           = round(pos["value"] - pos["cost"], 2)
            pos["pnl_pct"]       = round((price - pos["entry_price"]) / pos["entry_price"] * 100, 2)
        total_positions_value += pos.get("value", pos.get("cost", 0))

    portfolio["total_value"] = round(portfolio["cash"] + total_positions_value, 2)
    portfolio["pnl"]         = round(portfolio["total_value"] - STARTING_BALANCE, 2)
    portfolio["pnl_pct"]     = round(portfolio["pnl"] / STARTING_BALANCE * 100, 2)
    return portfolio

def execute_buy(portfolio, ticker, name, price, shares, trade_type, reasoning, score):
    """Execute a paper buy order."""
    cost = round(price * shares, 2)

    if cost > portfolio["cash"]:
        return False, "Insufficient cash"

    # Max position check
    max_allowed = portfolio["total_value"] * MAX_POSITION_PCT
    if cost > max_allowed:
        shares = int(max_allowed / price)
        cost   = round(price * shares, 2)
        if shares == 0:
            return False, "Position too small"

    stop_price = round(price * (1 + STOP_LOSS_PCT), 2)

    portfolio["cash"] = round(portfolio["cash"] - cost, 2)
    portfolio["positions"][ticker] = {
        "ticker":        ticker,
        "name":          name,
        "shares":        shares,
        "entry_price":   price,
        "current_price": price,
        "cost":          cost,
        "value":         cost,
        "pnl":           0.0,
        "pnl_pct":       0.0,
        "stop_loss":     stop_price,
        "trade_type":    trade_type,
        "score":         score,
        "reasoning":     reasoning,
        "entry_date":    datetime.utcnow().isoformat(),
    }

    portfolio["trades_count"] += 1

    # Log trade
    trades = load_trades()
    trades.insert(0, {
        "type":       "BUY",
        "ticker":     ticker,
        "name":       name,
        "shares":     shares,
        "price":      price,
        "cost":       cost,
        "trade_type": trade_type,
        "score":      score,
        "reasoning":  reasoning,
        "date":       datetime.utcnow().isoformat(),
    })
    save_trades(trades)

    return True, f"Bought {shares} shares of {ticker} at ${price} (${cost:,.0f})"

def execute_sell(portfolio, ticker, price, reason):
    """Execute a paper sell order."""
    if ticker not in portfolio["positions"]:
        return False, f"{ticker} not in portfolio"

    pos    = portfolio["positions"][ticker]
    shares = pos["shares"]
    cost   = pos["cost"]
    value  = round(price * shares, 2)
    pnl    = round(value - cost, 2)
    pnl_pct = round((price - pos["entry_price"]) / pos["entry_price"] * 100, 2)

    portfolio["cash"] = round(portfolio["cash"] + value, 2)

    if pnl > 0:
        portfolio["wins"] += 1
    else:
        portfolio["losses"] += 1

    del portfolio["positions"][ticker]

    # Log trade
    trades = load_trades()
    trades.insert(0, {
        "type":       "SELL",
        "ticker":     ticker,
        "name":       pos["name"],
        "shares":     shares,
        "entry_price":pos["entry_price"],
        "sell_price": price,
        "pnl":        pnl,
        "pnl_pct":    pnl_pct,
        "reason":     reason,
        "trade_type": pos["trade_type"],
        "date":       datetime.utcnow().isoformat(),
    })
    save_trades(trades)
    portfolio["trades_count"] += 1

    return True, f"Sold {ticker} at ${price} | P&L: ${pnl:+,.0f} ({pnl_pct:+.1f}%)"

def check_stop_losses(portfolio, current_prices):
    """Check and trigger -7% stop losses."""
    triggered = []
    for ticker, pos in list(portfolio["positions"].items()):
        price = current_prices.get(ticker)
        if price and price <= pos["stop_loss"]:
            ok, msg = execute_sell(portfolio, ticker, price, f"STOP LOSS triggered at ${price}")
            if ok:
                triggered.append(f"STOP LOSS: {ticker} at ${price} | -7%")
    return triggered
