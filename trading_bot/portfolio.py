from trading_bot.logger import logger

class Portfolio:
    def __init__(self, start_capital=100.0):
        self.initial_capital = start_capital
        self.capital = start_capital
        self.positions = {}  # symbol -> amount
        logger.info(f"Initialized Portfolio with Capital: {self.capital}")

    def update(self, trade_result):
        """
        Update portfolio based on trade result from Exchange.
        trade_result: dict returned by Exchange.execute_order
        """
        if not trade_result or trade_result.get('status') != 'filled':
            logger.warning("Trade update failed: Invalid trade result")
            return

        symbol = trade_result['symbol']
        amount = trade_result['amount']
        total_cost_or_revenue = trade_result['total']
        trade_type = trade_result['type']

        if trade_type == 'buy':
            if self.capital >= total_cost_or_revenue:
                self.capital -= total_cost_or_revenue
                self.positions[symbol] = self.positions.get(symbol, 0.0) + amount
                logger.info(f"Portfolio Updated (BUY): Cash={self.capital:.2f}, {symbol}={self.positions[symbol]}")
            else:
                logger.error(f"Insufficient funds for BUY: Need {total_cost_or_revenue}, Have {self.capital}")

        elif trade_type == 'sell':
            current_position = self.positions.get(symbol, 0.0)
            if current_position >= amount:
                self.capital += total_cost_or_revenue
                self.positions[symbol] -= amount
                if self.positions[symbol] <= 1e-9: # Clean up small floating point residues
                    del self.positions[symbol]
                logger.info(f"Portfolio Updated (SELL): Cash={self.capital:.2f}, {symbol}={self.positions.get(symbol, 0.0)}")
            else:
                logger.error(f"Insufficient position for SELL: Need {amount} {symbol}, Have {current_position}")

    def get_total_value(self, current_prices):
        """
        Calculate total portfolio value based on current market prices.
        current_prices: dict, symbol -> price
        """
        value = self.capital
        for symbol, amount in self.positions.items():
            price = current_prices.get(symbol, 0.0)
            value += amount * price
        return value

    def get_position(self, symbol):
        return self.positions.get(symbol, 0.0)
