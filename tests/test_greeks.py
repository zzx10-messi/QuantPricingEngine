from src.instruments import EuropeanOption
from src.market import MarketData
from src.models import BlackScholes
from src.risk import Greeks


def test_call_greeks():
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
    greeks = Greeks(model)

    assert abs(greeks.delta(option, market) - 0.636831) < 1e-5
    assert abs(greeks.gamma(option, market) - 0.018762) < 1e-5
    assert abs(greeks.vega(option, market) - 37.524035) < 1e-5
    assert abs(greeks.theta(option, market) - (-6.414028)) < 1e-5
    assert abs(greeks.rho(option, market) - 53.232482) < 1e-5


def test_put_greeks():
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
    greeks = Greeks(model)

    assert abs(greeks.delta(option, market) - (-0.363169)) < 1e-5
    assert abs(greeks.gamma(option, market) - 0.018762) < 1e-5
    assert abs(greeks.vega(option, market) - 37.524035) < 1e-5
    assert abs(greeks.theta(option, market) - (-1.657880)) < 1e-5
    assert abs(greeks.rho(option, market) - (-41.890461)) < 1e-5


def test_gamma_and_vega_are_identical_for_call_and_put():
    market = MarketData(
        spot=100,
        rate=0.05,
        volatility=0.2,
    )
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

    model = BlackScholes()
    greeks = Greeks(model)

    assert greeks.gamma(call, market) == greeks.gamma(put, market)
    assert greeks.vega(call, market) == greeks.vega(put, market)
