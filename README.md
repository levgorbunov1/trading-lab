# trading-lab
Experiments with algorithmic trading.

# Trading Bot Strategy

This trading bot uses a simple swing trading strategy to execute trades on the Alpaca paper trading API. The strategy is designed for low-frequency, ephemeral execution environments such as GitHub Actions.

# How It Works

1. Buy Signal

The bot buys the selected stock if it does not currently hold a position.

The entry price is recorded in a state.json file to track the position across runs.

2. Take Profit

If the stock price increases by +2% relative to the entry price, the bot automatically sells to lock in profits.

3. Stop Loss

If the stock price drops by -20% relative to the entry price, the bot automatically sells to limit losses.

4. Hold

If the price is between the stop loss and take profit thresholds, the bot holds the position until the next scheduled run.