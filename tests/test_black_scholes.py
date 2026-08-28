import numpy as np

from option_pricing.analytical import BlackScholes
from option_pricing.common import MarketData
from option_pricing.products import EuropeanOption


def test_european_call_price():
    option = EuropeanOption(
        strike=100,
        maturity=1,
        option_type="call",
    )
    market = MarketData(
        spot=100,
        rate=0.05,
        volatility=0.2,
    )

    model = BlackScholes()
    price = model.price(option, market)

    expected_price = 10.450584
    assert abs(price - expected_price) < 1e-5


def test_european_put_price():
    option = EuropeanOption(
        strike=100,
        maturity=1,
        option_type="put",
    )
    market = MarketData(
        spot=100,
        rate=0.05,
        volatility=0.2,
    )

    model = BlackScholes()
    price = model.price(option, market)

    expected_price = 5.573526
    assert abs(price - expected_price) < 1e-5


def test_put_call_parity():
    call = EuropeanOption(
        strike=100,
        maturity=1,
        option_type="call",
    )
    put = EuropeanOption(
        strike=100,
        maturity=1,
        option_type="put",
    )
    market = MarketData(
        spot=100,
        rate=0.05,
        volatility=0.2,
    )

    model = BlackScholes()
    call_price = model.price(call, market)
    put_price = model.price(put, market)

    # C - P = S - K * exp(-rT)
    expected_diff = market.spot - call.strike * np.exp(-market.rate * call.maturity)
    assert abs((call_price - put_price) - expected_diff) < 1e-5


def test_zero_volatility_uses_discounted_intrinsic_value():
    call = EuropeanOption(strike=100, maturity=1, option_type="call")
    put = EuropeanOption(strike=100, maturity=1, option_type="put")
    market = MarketData(spot=100, rate=0.05, volatility=0.0)
    model = BlackScholes()
    discounted_strike = 100 * np.exp(-0.05)

    assert model.price(call, market) == max(100 - discounted_strike, 0.0)
    assert model.price(put, market) == max(discounted_strike - 100, 0.0)
