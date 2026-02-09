from trading_bot.strategy import Strategy
from collections import deque

class SimpleMAStrategy(Strategy):
    def __init__(self, name, portfolio, symbol, short_window=10, long_window=30):
        super().__init__(name, portfolio)
        self.symbol = symbol
        self.short_window = short_window
        self.long_window = long_window
        self.prices = deque(maxlen=long_window)

    def on_data(self, price):
        self.prices.append(price)

        if len(self.prices) < self.long_window:
            return None # Not enough data

        short_ma = sum(list(self.prices)[-self.short_window:]) / self.short_window
        long_ma = sum(self.prices) / self.long_window

        self.log(f"Price: {price:.2f}, Short MA: {short_ma:.2f}, Long MA: {long_ma:.2f}")

        action = None

        # Simple Crossover Logic
        current_position = self.portfolio.get_position(self.symbol)

        if short_ma > long_ma and current_position <= 1e-9:
            # Buy signal
            amount_to_buy = self.portfolio.capital / price * 0.95 # Use 95% of capital to cover fees
            if amount_to_buy > 0:
                action = {'type': 'buy', 'symbol': self.symbol, 'amount': amount_to_buy, 'price': price}
                self.log(f"Signal: BUY {amount_to_buy:.4f} {self.symbol}")

        elif short_ma < long_ma and current_position > 1e-9:
            # Sell signal
            amount_to_sell = current_position
            if amount_to_sell > 0:
                action = {'type': 'sell', 'symbol': self.symbol, 'amount': amount_to_sell, 'price': price}
                self.log(f"Signal: SELL {amount_to_sell:.4f} {self.symbol}")

        return action
