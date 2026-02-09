import itertools
import csv
import os
from trading_bot.exchange import Exchange
from trading_bot.portfolio import Portfolio
from trading_bot.engine import TradingEngine
from trading_bot.logger import logger

class Optimizer:
    def __init__(self, strategy_class, param_grid, data, symbol='BTC/USD', start_capital=100.0, fee_rate=0.001):
        """
        Initialize the Optimizer.

        Args:
            strategy_class: The class of the strategy to optimize.
            param_grid: Dictionary of parameters to test (e.g., {'short_window': [5, 10], 'long_window': [20, 30]})
            data: List of price data dictionaries.
            symbol: The symbol to trade.
            start_capital: Initial capital for each run.
            fee_rate: Trading fee rate.
        """
        self.strategy_class = strategy_class
        self.param_grid = param_grid
        self.data = data
        self.symbol = symbol
        self.start_capital = start_capital
        self.fee_rate = fee_rate
        self.results = []

    def run(self):
        """
        Run the optimization process.
        Returns:
            dict: Best parameter set.
        """
        keys = self.param_grid.keys()
        values = self.param_grid.values()
        combinations = list(itertools.product(*values))

        logger.info(f"Starting optimization with {len(combinations)} combinations...")

        best_performance = -float('inf')
        best_params = None

        for i, combination in enumerate(combinations):
            params = dict(zip(keys, combination))

            # Validate parameters (e.g., short_window < long_window)
            if 'short_window' in params and 'long_window' in params:
                if params['short_window'] >= params['long_window']:
                    continue

            # Run Simulation
            exchange = Exchange(name="OptimizerExchange", fee_rate=self.fee_rate)
            portfolio = Portfolio(start_capital=self.start_capital)

            # Create strategy with unpacked parameters
            # Note: We assume strategy init accepts these kwargs + standard args
            strategy_name = f"Run_{i}"
            strategy = self.strategy_class(name=strategy_name, portfolio=portfolio, symbol=self.symbol, **params)

            engine = TradingEngine(exchange, [strategy])
            engine.run_backtest(self.data)

            # Evaluate
            # Use current price (last data point) to value position
            last_price = self.data[-1].get(self.symbol, 0) if self.data else 0
            current_prices = {self.symbol: last_price}
            final_value = portfolio.get_total_value(current_prices)

            result = {
                'params': params,
                'final_value': final_value,
                'roi': (final_value - self.start_capital) / self.start_capital * 100
            }
            self.results.append(result)

            logger.info(f"Run {i}: Params={params} | Final Value={final_value:.2f}")

            if final_value > best_performance:
                best_performance = final_value
                best_params = params

        logger.info(f"Optimization Complete. Best Value: {best_performance:.2f} with Params: {best_params}")
        self.save_results()
        return best_params

    def save_results(self, filename='optimization_results.csv'):
        """Save all run results to a CSV file."""
        if not self.results:
            return

        # Flatten the dictionary for CSV
        fieldnames = ['run_id', 'final_value', 'roi'] + list(self.results[0]['params'].keys())

        with open(filename, 'w', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()

            for i, res in enumerate(self.results):
                row = {
                    'run_id': i,
                    'final_value': res['final_value'],
                    'roi': res['roi']
                }
                row.update(res['params'])
                writer.writerow(row)

        logger.info(f"Optimization results saved to {filename}")
