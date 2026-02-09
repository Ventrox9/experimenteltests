from trading_bot.data.loader import fetch_crypto_data
from trading_bot.strategies.simple_ma import SimpleMAStrategy
from trading_bot.optimizer import Optimizer
from trading_bot.logger import logger
from trading_bot.engine import TradingEngine
from trading_bot.exchange import Exchange
from trading_bot.portfolio import Portfolio

def main():
    logger.info("Initializing Trading Bot Optimization...")

    # 1. Fetch Real Data (Coinbase or Fallback)
    days = 12 # Coinbase returns 300 candles (12.5 days). Let's use 12.
    symbol = "BTC/USD"
    data = fetch_crypto_data('bitcoin', days=days)

    if not data:
        logger.error("No data available. Exiting.")
        return

    # 2. Define Parameter Grid
    # We want to find the best Moving Average window combination
    param_grid = {
        'short_window': [5, 10, 15, 20],
        'long_window': [25, 30, 40, 50, 60]
    }

    # 3. Run Optimization
    logger.info("Running Strategy Optimization...")
    optimizer = Optimizer(SimpleMAStrategy, param_grid, data, symbol=symbol, start_capital=100.0)
    best_params = optimizer.run()

    if not best_params:
        logger.error("Optimization failed to find parameters.")
        return

    logger.info(f"=== WINNER: Best Parameters: {best_params} ===")

    # 4. Run Best Strategy with Detailed Logs
    logger.info("Running final simulation with best parameters...")

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
    print(f"Optimization data saved to 'optimization_results.csv'")
    print("="*40 + "\n")

if __name__ == "__main__":
    main()
