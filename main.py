import random
import math
from trading_bot.exchange import Exchange
from trading_bot.portfolio import Portfolio
from trading_bot.strategies.simple_ma import SimpleMAStrategy
from trading_bot.engine import TradingEngine
from trading_bot.logger import logger

def generate_dummy_data(length=100):
    """Generate simple oscillating price data."""
    prices = []
    base_price = 100
    for i in range(length):
        price = base_price + 10 * math.sin(i / 5.0) + random.uniform(-1, 1)
        prices.append({'BTC/USD': max(10, price)})
    return prices

def main():
    logger.info("Initializing Trading Bot Simulation...")

    # 1. Setup Exchange (Simulated)
    exchange = Exchange(name="SimulatedExchange", fee_rate=0.001) # 0.1% fee

    # 2. Setup Strategies
    # Strategy 1: Standard MA
    portfolio1 = Portfolio(start_capital=100.0)
    strategy1 = SimpleMAStrategy(name="MA_Strategy_Standard", portfolio=portfolio1, symbol="BTC/USD", short_window=5, long_window=20)

    # Strategy 2: Faster MA (Parallel Execution Concept)
    portfolio2 = Portfolio(start_capital=100.0)
    strategy2 = SimpleMAStrategy(name="MA_Strategy_Fast", portfolio=portfolio2, symbol="BTC/USD", short_window=3, long_window=10)

    strategies = [strategy1, strategy2]

    # 3. Setup Engine
    engine = TradingEngine(exchange, strategies)

    # 4. Run Backtest with Dummy Data
    logger.info("Generating dummy market data...")
    data = generate_dummy_data(length=200)

    engine.run_backtest(data)

if __name__ == "__main__":
    main()
