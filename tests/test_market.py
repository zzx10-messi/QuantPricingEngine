import pytest

from src.market import MarketData


def test_valid_market_data():
    market = MarketData(
        spot=100,
        rate=0.05,
        volatility=0.2,
    )

    assert market.spot == 100
    assert market.rate == 0.05
    assert market.volatility == 0.2


def test_invalid_spot():
    with pytest.raises(ValueError):
        MarketData(
            spot=0,
            rate=0.05,
            volatility=0.2,
        )


def test_invalid_rate():
    with pytest.raises(ValueError):
        MarketData(
            spot=100,
            rate=-0.01,
            volatility=0.2,
        )


def test_invalid_volatility():
    with pytest.raises(ValueError):
        MarketData(
            spot=100,
            rate=0.05,
            volatility=-0.2,
        )
