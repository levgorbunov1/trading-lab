import os
import json
from datetime import datetime, timezone
from alpaca_trade_api import REST

API_KEY = os.environ["API_KEY"]
SECRET_KEY = os.environ["API_SECRET"]

BASE_URL = "https://paper-api.alpaca.markets"

api = REST(API_KEY, SECRET_KEY, BASE_URL)

symbol = "AAPL"
STATE_FILE = "state.json"


def now():
    return datetime.now(timezone.utc).isoformat()


def load_state():
    if not os.path.exists(STATE_FILE):
        return {
            "symbol": symbol,
            "initial_price": None,
            "position_qty": 0,
            "last_trade": None,
            "last_updated": None
        }

    with open(STATE_FILE, "r") as f:
        return json.load(f)


def save_state(state):
    state["last_updated"] = now()

    with open(STATE_FILE, "w") as f:
        json.dump(state, f, indent=2)


def get_price():
    trade = api.get_latest_trade(symbol)
    return trade.price


def buy(qty=1):
    api.submit_order(
        symbol=symbol,
        qty=qty,
        side="buy",
        type="market",
        time_in_force="gtc"
    )


def sell(qty=1):
    api.submit_order(
        symbol=symbol,
        qty=qty,
        side="sell",
        type="market",
        time_in_force="gtc"
    )


def run():
    state = load_state()

    initial_price = state["initial_price"]
    qty = state["position_qty"]

    price = get_price()

    print("Current price:", price)
    print("Initial price:", initial_price)
    print("Position qty:", qty)

    # No position -> buy
    if qty == 0:
        print("No position, buying...")

        buy()

        state["initial_price"] = price
        state["position_qty"] = 1
        state["last_trade"] = "buy"

        save_state(state)

        print("Bought at", price)
        return

    change = (price - initial_price) / initial_price

    print("Change:", change)

    # Take profit
    if change >= 0.05:
        print("Take profit triggered")

        sell(qty)

        state["initial_price"] = None
        state["position_qty"] = 0
        state["last_trade"] = "sell"

        save_state(state)

    # Stop loss
    elif change <= -0.10:
        print("Stop loss triggered")

        sell(qty)

        state["initial_price"] = None
        state["position_qty"] = 0
        state["last_trade"] = "sell"

        save_state(state)

    else:
        print("Hold position")


if __name__ == "__main__":
    run()