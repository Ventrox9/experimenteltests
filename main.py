from trading_bot.data.loader import fetch_crypto_data
from trading_bot.strategies.simple_ma import SimpleMAStrategy
from trading_bot.optimizer import Optimizer
from trading_bot.logger import logger
from trading_bot.engine import TradingEngine
from trading_bot.exchange import Exchange
from trading_bot.portfolio import Portfolio
from trading_bot.realtime_exchange import RealTimeExchange
from trading_bot.live_engine import LiveTradingEngine
import sys
import time

def run_live(symbol="BTC/USD", interval=60):
    logger.info("Initializing Live Trading Mode...")

    # 1. Warmup Data
    # We need to fill the strategy's buffer so it can calculate MAs from the start
    # Assume we need at least 50 points (max MA window).
    logger.info("Fetching warmup data (12 days)...")
    warmup_data = fetch_crypto_data('bitcoin', days=12)

    if not warmup_data:
        logger.error("Could not fetch warmup data.")
        return

    # 2. Get Best Params via Quick Optimization
    # Optimize on the last 12 days to find the best current strategy
    param_grid = {
        'short_window': [5, 10, 20],
        'long_window': [25, 40, 60]
    }

    logger.info("Running optimization on recent data...")
    optimizer = Optimizer(SimpleMAStrategy, param_grid, warmup_data, symbol=symbol, start_capital=100.0)
    best_params = optimizer.run()

    if not best_params:
        logger.error("Optimization failed.")
        return

    logger.info(f"Using Strategy Parameters: {best_params}")

    # 3. Setup Live Environment
    exchange = RealTimeExchange(name="CoinbaseLive", fee_rate=0.001)
    portfolio = Portfolio(start_capital=100.0)
    strategy = SimpleMAStrategy(name="LiveMAStrategy", portfolio=portfolio, symbol=symbol, **best_params)

    # 4. Fill Strategy Buffer with Warmup Data
    logger.info("Warming up strategy indicators...")
    for tick in warmup_data:
        price = tick.get(symbol)
        if price:
            strategy.on_data(price) # This updates the deque but doesn't trade because price is historical?
            # Actually, SimpleMAStrategy.on_data WILL trade if conditions met.
            # But since we are feeding historical data, we want to IGNORE trades during warmup.
            # Hack: Temporarily disable portfolio updates or clear trades after warmup.
            # Better: Pass a flag 'warmup=True' to on_data or just reset portfolio.

    # Reset Portfolio to start fresh (capital=100) but keep strategy internal state (deque filled)
    portfolio.capital = 100.0
    portfolio.positions = {}
    strategy.position = 0 # Reset trading position state
    logger.info("Strategy warmed up. Starting live loop...")

    # 5. Start Live Engine
    engine = LiveTradingEngine(exchange, [strategy], interval=interval)
    engine.start()

def main():
    if len(sys.argv) > 1 and sys.argv[1] == '--live':
        run_live()
    else:
        logger.info("Running Backtest/Optimization Mode (Default)...")
        # Reuse existing main logic
        from trading_bot.data.loader import fetch_crypto_data

        days = 12
        symbol = "BTC/USD"
        data = fetch_crypto_data('bitcoin', days=days)

        if not data:
            logger.error("No data available.")
            return

        param_grid = {
            'short_window': [5, 10, 15, 20],
            'long_window': [25, 30, 40, 50, 60]
        }

        logger.info("Running Strategy Optimization...")
        optimizer = Optimizer(SimpleMAStrategy, param_grid, data, symbol=symbol, start_capital=100.0)
        best_params = optimizer.run()

        if not best_params:
            logger.error("Optimization failed.")
            return

        logger.info(f"=== WINNER: Best Parameters: {best_params} ===")

        logger.info("Running final simulation...")
        exchange = Exchange(name="FinalExchange", fee_rate=0.001)
        portfolio = Portfolio(start_capital=100.0)
        strategy = SimpleMAStrategy(name="BestStrategy", portfolio=portfolio, symbol=symbol, **best_params)

        engine = TradingEngine(exchange, [strategy])
        engine.run_backtest(data)

        # Final Report
        last_price = data[-1].get(symbol, 0)
        final_value = portfolio.get_total_value({symbol: last_price})
        roi = (final_value - 100.0) / 100.0 * 100

        print("\n" + "="*40)
        print(f"FINAL RESULT ({symbol})")
        print(f"Strategy: Simple Moving Average")
        print(f"Best Params: {best_params}")
        print(f"Final Capital: {final_value:.2f}")
        print(f"ROI: {roi:.2f}%")
        print("="*40 + "\n")

if __name__ == "__main__":
    main()
