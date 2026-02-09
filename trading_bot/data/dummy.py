import random
import math

def generate_dummy_data(length=100):
    """Generate simple oscillating price data."""
    prices = []
    base_price = 100
    for i in range(length):
        price = base_price + 10 * math.sin(i / 5.0) + random.uniform(-1, 1)
        prices.append({'BTC/USD': max(10, price), 'timestamp': i})
    return prices
