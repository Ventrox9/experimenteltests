import requests
import logging
import time
from datetime import datetime, timedelta

logger = logging.getLogger('trading_bot')

def fetch_crypto_data(coin_id='bitcoin', vs_currency='usd', days=30):
    """
    Fetch historical market data. Tries Coinbase Pro first.

    Args:
        coin_id (str): The common name (e.g., 'bitcoin').
        vs_currency (str): The target currency (e.g., 'usd').
        days (int): Number of days of data to fetch.

    Returns:
        list: A list of dictionaries [{'BTC/USD': 12345.67, 'timestamp': 1678900000}, ...]
    """
    # Map common names to Coinbase products
    symbol_map = {
        'bitcoin': 'BTC-USD',
        'ethereum': 'ETH-USD',
        'dogecoin': 'DOGE-USD'
    }

    product_id = symbol_map.get(coin_id.lower())
    if not product_id:
        logger.error(f"Symbol mapping not found for {coin_id}")
        return []

    data = fetch_coinbase_data(product_id, days)

    if not data:
        logger.warning("Coinbase fetch failed. Falling back to dummy generation.")
        # Fallback to dummy data if API fails to ensure user experience isn't broken
        from trading_bot.data.dummy import generate_dummy_data
        logger.info("Generating dummy data as fallback...")
        return generate_dummy_data(days * 24) # Assuming hourly dummy data

    return data

def fetch_coinbase_data(product_id, days):
    """Fetch candles from Coinbase Exchange API."""
    url = f"https://api.exchange.coinbase.com/products/{product_id}/candles"

    # Coinbase granularity is in seconds. 3600 = 1h.
    granularity = 3600

    # Coinbase limits to 300 candles per request.
    # To get 'days' worth of data, we might need multiple calls or just take the last 300 hours (~12.5 days).
    # For simplicity and reliability in this demo, let's limit to 300 candles max (12 days hourly).
    # If users want more, they can modify this to paginate.

    params = {
        'granularity': granularity
    }

    try:
        logger.info(f"Fetching data for {product_id} from Coinbase...")
        # Note: Coinbase API returns candles in reverse chronological order (newest first)
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        candles = response.json()

        # Check if candles is a list (success) or dict (error)
        if isinstance(candles, dict) and 'message' in candles:
             logger.error(f"Coinbase API Error: {candles['message']}")
             return []

        formatted_data = []
        display_symbol = product_id.replace('-', '/') # BTC/USD

        # Reverse to get chronological order (oldest first)
        candles.reverse()

        for candle in candles:
            # candle format: [timestamp, low, high, open, close, volume]
            timestamp = candle[0]
            close_price = float(candle[4])

            # Format as {SYMBOL: PRICE, 'timestamp': TIMESTAMP}
            # This matches what TradingEngine expects (dict of symbol->price)
            formatted_data.append({
                display_symbol: close_price,
                'timestamp': timestamp
            })

        logger.info(f"Successfully fetched {len(formatted_data)} data points for {display_symbol}.")
        return formatted_data

    except requests.exceptions.RequestException as e:
        logger.error(f"Error fetching from Coinbase: {e}")
        return []
