import pytest
from trading_bot.portfolio import Portfolio

class TestPortfolio:
    def test_initialization(self):
        p = Portfolio(start_capital=100.0)
        assert p.capital == 100.0
        assert p.positions == {}

    def test_buy_update(self):
        p = Portfolio(start_capital=1000.0)
        # Simulate a buy trade result
        trade_result = {
            'status': 'filled',
            'type': 'buy',
            'symbol': 'BTC/USD',
            'amount': 0.1,
            'price': 1000.0,
            'fee': 1.0,
            'total': 101.0 # 100 + 1
        }
        p.update(trade_result)

        assert p.capital == 899.0 # 1000 - 101
        assert p.positions['BTC/USD'] == 0.1

    def test_sell_update(self):
        p = Portfolio(start_capital=0.0)
        p.positions['BTC/USD'] = 0.5

        trade_result = {
            'status': 'filled',
            'type': 'sell',
            'symbol': 'BTC/USD',
            'amount': 0.2,
            'price': 1000.0,
            'fee': 2.0,
            'total': 198.0 # 200 - 2
        }
        p.update(trade_result)

        assert p.capital == 198.0
        assert abs(p.positions['BTC/USD'] - 0.3) < 1e-9

    def test_insufficient_funds(self):
        p = Portfolio(start_capital=50.0)
        trade_result = {
            'status': 'filled',
            'type': 'buy',
            'symbol': 'BTC/USD',
            'amount': 0.1,
            'price': 1000.0,
            'fee': 1.0,
            'total': 101.0
        }
        p.update(trade_result)

        # Should not change
        assert p.capital == 50.0
        assert 'BTC/USD' not in p.positions

    def test_insufficient_position(self):
        p = Portfolio()
        trade_result = {
            'status': 'filled',
            'type': 'sell',
            'symbol': 'BTC/USD',
            'amount': 1.0,
            'price': 100.0,
            'total': 100.0
        }
        p.update(trade_result)

        # Should not change
        assert p.capital == 100.0 # Default start capital
        assert p.positions == {}

    def test_total_value(self):
        p = Portfolio(start_capital=100.0)
        p.capital = 50.0
        p.positions['A'] = 10
        p.positions['B'] = 5

        prices = {'A': 2.0, 'B': 4.0}
        value = p.get_total_value(prices)

        # 50 + (10*2) + (5*4) = 50 + 20 + 20 = 90
        assert value == 90.0
