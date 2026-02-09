import concurrent.futures
from trading_bot.logger import logger

class TradingEngine:
    def __init__(self, exchange, strategies):
        self.exchange = exchange
        self.strategies = strategies # List of Strategy instances
        logger.info(f"Initialized Trading Engine with {len(strategies)} strategies")

    def run_step(self, price_data):
        """
        Execute one step of the simulation.
        price_data: dict, symbol -> price
        """
        # In a real scenario, we might want to run strategies in parallel
        # For this simulation, we iterate sequentially for simplicity and safety

        for strategy in self.strategies:
            # Assuming single symbol strategy for now
            symbol = strategy.symbol
            current_price = price_data.get(symbol)

            if current_price is None:
                continue

            # Get action from strategy
            action = strategy.on_data(current_price)

            if action:
                # Execute order
                order_type = action['type']
                amount = action['amount']
                price = action['price']

                trade_result = self.exchange.execute_order(order_type, symbol, amount, price)

                if trade_result:
                    strategy.portfolio.update(trade_result)
                    logger.info(f"Strategy {strategy.name} Executed Trade: {trade_result}")

    def run_backtest(self, data_feed):
        """
        Run a backtest over a data feed.
        data_feed: list of dicts or iterable yielding price_data
        """
        logger.info("Starting Backtest...")
        for price_data in data_feed:
            self.run_step(price_data)

        logger.info("Backtest Completed.")
        self.print_summary()

    def print_summary(self):
        logger.info("=== Performance Summary ===")
        for strategy in self.strategies:
            portfolio_value = strategy.portfolio.get_total_value({}) # Pass current prices if needed, here assuming sold out or just cash
            # To get accurate final value including positions, we need the last price.
            # For now, let's just print the cash balance and positions.

            logger.info(f"Strategy: {strategy.name}")
            logger.info(f"  Final Capital: {strategy.portfolio.capital:.2f}")
            logger.info(f"  Positions: {strategy.portfolio.positions}")
