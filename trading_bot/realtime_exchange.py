from trading_bot.exchange import Exchange
from trading_bot.data.loader import fetch_crypto_data
from trading_bot.logger import logger
import time

class RealTimeExchange(Exchange):
    def __init__(self, name="CoinbaseRealTime", fee_rate=0.001):
        super().__init__(name, fee_rate)
        # Note: We are simulating execution, but using REAL prices.
        # So "execute_order" remains from simulated Exchange.
        # But we implement "get_current_price" to hit the API.

    def get_current_price(self, symbol="BTC/USD"):
        """
        Fetch the current price from Coinbase API (using loader.py logic).
        For simplicity, we call fetch_crypto_data with days=1 (or less) and take the latest.
        Ideally we would use the Ticker endpoint.
        """
        try:
            # Reusing fetch_crypto_data for simplicity and robustness
            # It returns a list of candles. Last one is usually "current" or close to it.
            # But candles update every hour or minute.
            # Let's try to get a more "live" price if possible.

            # Coinbase Product Ticker Endpoint
            # https://api.exchange.coinbase.com/products/{product_id}/ticker
            # BTC-USD
            product_id = symbol.replace('/', '-')
            url = f"https://api.exchange.coinbase.com/products/{product_id}/ticker"

            import requests
            response = requests.get(url, timeout=5)
            response.raise_for_status()
            ticker = response.json()

            if 'price' in ticker:
                price = float(ticker['price'])
                logger.info(f"Current Price {symbol}: {price}")
                return price

            logger.warning(f"Could not parse ticker for {symbol}")
            return None

        except Exception as e:
            logger.error(f"Error fetching live price for {symbol}: {e}")
            return None
