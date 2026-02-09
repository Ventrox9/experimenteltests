import datetime

class StatusLogger:
    def __init__(self, filename='live_status.txt'):
        self.filename = filename

    def update(self, price, strategy):
        """
        Update the status file with the latest bot state.

        Args:
            price (float): Current market price.
            strategy (Strategy): The strategy instance being tracked.
        """
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Calculate financials
        portfolio = strategy.portfolio
        cash = portfolio.capital
        position_amount = portfolio.get_position(strategy.symbol)
        position_value = position_amount * price
        total_value = cash + position_value
        initial_capital = portfolio.initial_capital
        profit_loss = total_value - initial_capital
        roi = (profit_loss / initial_capital) * 100

        # Determine status
        status = "HOLD"
        if position_amount > 0:
            status = "LONG (Invested)"
        else:
            status = "NEUTRAL (Cash)"

        content = f"""
========================================
TRADING BOT LIVE STATUS
========================================
Timestamp:      {timestamp}
Market:         {strategy.symbol}
Current Price:  ${price:.2f}

STRATEGY:       {strategy.name}
Status:         {status}
----------------------------------------
FINANCIALS
----------------------------------------
Cash:           ${cash:.2f}
Assets ({strategy.symbol}): {position_amount:.6f}
Asset Value:    ${position_value:.2f}
----------------------------------------
TOTAL EQUITY:   ${total_value:.2f}
PROFIT/LOSS:    ${profit_loss:+.2f} ({roi:+.2f}%)
========================================
Last Update: {timestamp}
"""
        try:
            with open(self.filename, 'w') as f:
                f.write(content)
        except Exception as e:
            print(f"Error writing status file: {e}")
