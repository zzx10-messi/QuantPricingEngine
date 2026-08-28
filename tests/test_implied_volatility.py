import pytest

from option_pricing.analytical import BlackScholes
from option_pricing.analytics import ImpliedVolatility
from option_pricing.common import ConvergenceError, MarketData
from option_pricing.products import EuropeanOption


def _make_setup():
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
    return option, market, model


def test_solve_round_trip_brent():
    option, market, model = _make_setup()
    price = model.price(option, market)

    solver = ImpliedVolatility(model)
    iv = solver.solve(option, market, price, method="brent")

    assert abs(iv - 0.2) < 1e-4


def test_solve_round_trip_bisection():
    option, market, model = _make_setup()
    price = model.price(option, market)

    solver = ImpliedVolatility(model)
    iv = solver.solve(option, market, price, method="bisection")

    assert abs(iv - 0.2) < 1e-4


def test_solve_round_trip_newton():
    option, market, model = _make_setup()
    price = model.price(option, market)

    solver = ImpliedVolatility(model)
    iv = solver.solve(option, market, price, method="newton")

    assert abs(iv - 0.2) < 1e-4


def test_solve_put_option():
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

    solver = ImpliedVolatility(model)
    iv = solver.solve(option, market, price)

    assert abs(iv - 0.2) < 1e-4


def test_all_methods_agree():
    option, market, model = _make_setup()
    price = model.price(option, market)

    solver = ImpliedVolatility(model)

    results = {
        method: solver.solve(option, market, price, method=method)
        for method in ("brent", "bisection", "newton")
    }

    for iv in results.values():
        assert abs(iv - results["brent"]) < 1e-4


def test_invalid_target_price():
    option, market, model = _make_setup()
    solver = ImpliedVolatility(model)

    with pytest.raises(ValueError):
        solver.solve(option, market, target_price=-1.0)


def test_unknown_method():
    option, market, model = _make_setup()
    price = model.price(option, market)
    solver = ImpliedVolatility(model)

    with pytest.raises(ValueError):
        solver.solve(option, market, price, method="foo")


def test_bisection_reports_non_convergence():
    option, market, model = _make_setup()
    price = model.price(option, market)

    with pytest.raises(ConvergenceError):
        ImpliedVolatility(model).solve(
            option, market, price, method="bisection", max_iter=1
        )


def test_newton_is_safeguarded_when_initial_vega_is_zero():
    option = EuropeanOption(strike=20, maturity=0.01, option_type="call")
    market = MarketData(spot=100, rate=0.05, volatility=0.2)
    true_market = MarketData(spot=100, rate=0.05, volatility=4.0)
    model = BlackScholes()
    target = model.price(option, true_market)

    implied_vol = ImpliedVolatility(model).solve(
        option, market, target, method="newton"
    )

    assert abs(model.price(option, market.with_volatility(implied_vol)) - target) < 1e-6


def test_bracket_expands_above_initial_maximum():
    option, market, model = _make_setup()
    true_market = market.with_volatility(6.0)
    target = model.price(option, true_market)

    implied_vol = ImpliedVolatility(model).solve(option, market, target)

    assert abs(implied_vol - 6.0) < 1e-4


@pytest.mark.parametrize("target", [float("nan"), float("inf")])
def test_non_finite_target_is_rejected(target):
    option, market, model = _make_setup()
    with pytest.raises(ValueError):
        ImpliedVolatility(model).solve(option, market, target)


def test_price_outside_no_arbitrage_bounds_is_rejected():
    option, market, model = _make_setup()
    with pytest.raises(ValueError, match="target_price must be"):
        ImpliedVolatility(model).solve(option, market, market.spot)
