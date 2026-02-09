from trading_bot.logger import logger

class Exchange:
    def __init__(self, name="GenericExchange", fee_rate=0.001):
        """
        Initialize the exchange with a name and a fee rate.
        fee_rate: float, percentage of transaction value (e.g., 0.001 for 0.1%)
        """
        self.name = name
        self.fee_rate = fee_rate
        logger.info(f"Initialized Exchange: {self.name} with fee rate: {self.fee_rate}")

    def calculate_fee(self, amount, price):
        """Calculate the trading fee for a given transaction."""
        return amount * price * self.fee_rate

    def execute_order(self, order_type, symbol, amount, price):
        """
        Simulate order execution.
        order_type: 'buy' or 'sell'
        symbol: str, e.g., 'BTC/USD'
        amount: float, quantity to trade
        price: float, execution price

        Returns:
            dict: execution details including fee and total cost/revenue
        """
        if amount <= 0 or price <= 0:
            logger.error(f"Invalid order parameters: amount={amount}, price={price}")
            return None

        fee = self.calculate_fee(amount, price)
        total_value = amount * price

        if order_type.lower() == 'buy':
            cost = total_value + fee
            logger.info(f"EXECUTED BUY: {amount} {symbol} @ {price} | Fee: {fee:.4f} | Total Cost: {cost:.4f}")
            return {
                'status': 'filled',
                'type': 'buy',
                'symbol': symbol,
                'amount': amount,
                'price': price,
                'fee': fee,
                'total': cost # Total amount to be deducted from balance
            }
        elif order_type.lower() == 'sell':
            revenue = total_value - fee
            logger.info(f"EXECUTED SELL: {amount} {symbol} @ {price} | Fee: {fee:.4f} | Total Revenue: {revenue:.4f}")
            return {
                'status': 'filled',
                'type': 'sell',
                'symbol': symbol,
                'amount': amount,
                'price': price,
                'fee': fee,
                'total': revenue # Total amount to be added to balance
            }
        else:
            logger.error(f"Unknown order type: {order_type}")
            return None
