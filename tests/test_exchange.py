import pytest
from trading_bot.exchange import Exchange

class TestExchange:
    def test_fee_calculation(self):
        exchange = Exchange(fee_rate=0.01) # 1%
        fee = exchange.calculate_fee(amount=10, price=100)
        # 10 * 100 * 0.01 = 10
        assert fee == 10.0

    def test_buy_execution(self):
        exchange = Exchange(fee_rate=0.001) # 0.1%
        result = exchange.execute_order('buy', 'BTC/USD', 1.0, 10000.0)

        assert result['status'] == 'filled'
        assert result['type'] == 'buy'
        assert result['amount'] == 1.0
        assert result['price'] == 10000.0
        assert result['fee'] == 10.0 # 10000 * 0.001
        assert result['total'] == 10010.0 # 10000 + 10

    def test_sell_execution(self):
        exchange = Exchange(fee_rate=0.001) # 0.1%
        result = exchange.execute_order('sell', 'BTC/USD', 1.0, 10000.0)

        assert result['status'] == 'filled'
        assert result['type'] == 'sell'
        assert result['total'] == 9990.0 # 10000 - 10

    def test_invalid_order(self):
        exchange = Exchange()
        result = exchange.execute_order('buy', 'BTC/USD', -1, 100)
        assert result is None
