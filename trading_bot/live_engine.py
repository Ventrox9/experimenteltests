import time
from trading_bot.logger import logger

class LiveTradingEngine:
    def __init__(self, exchange, strategies, interval=60):
        """
        Initialize the Live Trading Engine.

        Args:
            exchange: Exchange instance (must implement get_current_price).
            strategies: List of Strategy instances.
            interval: Loop interval in seconds (default 60).
        """
        self.exchange = exchange
        self.strategies = strategies
        self.interval = interval
        self.is_running = False

    def start(self):
        """Start the live trading loop."""
        self.is_running = True
        logger.info(f"Starting Live Trading Engine (Interval: {self.interval}s)...")
        logger.info("Press Ctrl+C to stop.")

        try:
            while self.is_running:
                self.tick()
                time.sleep(self.interval)
        except KeyboardInterrupt:
            self.stop()

    def stop(self):
        """Stop the live trading loop."""
        self.is_running = False
        logger.info("Live Trading Engine stopped.")
        self.print_summary()

    def tick(self):
        """Execute one tick of the live loop."""
        try:
            # 1. Get current market prices for all relevant symbols
            # Assuming all strategies trade the same symbol for now or iterate
            symbols = set(s.symbol for s in self.strategies)
            current_prices = {}

            for symbol in symbols:
                price = self.exchange.get_current_price(symbol)
                if price:
                    current_prices[symbol] = price
                else:
                    logger.warning(f"Could not fetch current price for {symbol}")

            if not current_prices:
                return

            # 2. Update strategies
            for strategy in self.strategies:
                symbol = strategy.symbol
                price = current_prices.get(symbol)

                if price is None:
                    continue

                # Strategies expect just the price float in on_data for now
                # In a more advanced version, we might pass the full ticker dict
                action = strategy.on_data(price)

                if action:
                    # Execute order
                    order_type = action['type']
                    amount = action['amount']
                    price = action['price']

                    trade_result = self.exchange.execute_order(order_type, symbol, amount, price)

                    if trade_result:
                        strategy.portfolio.update(trade_result)
                        logger.info(f"LIVE TRADE: Strategy {strategy.name} Executed {order_type.upper()} {amount} {symbol} @ {price}")

        except Exception as e:
            logger.error(f"Error in live tick: {e}")

    def print_summary(self):
        logger.info("=== Live Session Summary ===")
        for strategy in self.strategies:
            # We need current price to value portfolio correctly
            # Try to fetch one last time
            price = self.exchange.get_current_price(strategy.symbol) or 0

            logger.info(f"Strategy: {strategy.name}")
            logger.info(f"  Cash: {strategy.portfolio.capital:.2f}")
            logger.info(f"  Positions: {strategy.portfolio.positions}")
            if price > 0:
                total_val = strategy.portfolio.get_total_value({strategy.symbol: price})
                logger.info(f"  Total Value (~{price}): {total_val:.2f}")
