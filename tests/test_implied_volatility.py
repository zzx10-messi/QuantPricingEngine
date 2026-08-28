import pytest
import numpy as np

from option_pricing.analytical import BlackScholes
from option_pricing.analytics import ImpliedVolatility
from option_pricing.common import ConvergenceError, MarketData, RootFindingMethod
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


def test_zero_implied_volatility_can_be_repriced():
    option, market, model = _make_setup()
    zero_vol_market = market.with_volatility(0.0)
    target = model.price(option, zero_vol_market)

    implied_vol = ImpliedVolatility(model).solve(option, market, target)

    assert implied_vol == 0.0
    assert model.price(option, market.with_volatility(implied_vol)) == target


def test_invalid_method_is_rejected_at_price_boundary():
    option, market, model = _make_setup()
    target = model.price(option, market.with_volatility(0.0))

    with pytest.raises(ValueError, match="Unknown root-finding method"):
        ImpliedVolatility(model).solve(option, market, target, method="foo")


def test_numpy_real_target_is_supported():
    option, market, model = _make_setup()
    target = np.float32(model.price(option, market))

    implied_vol = ImpliedVolatility(model).solve(option, market, target)

    assert abs(implied_vol - 0.2) < 1e-4


def test_newton_initial_guess_is_independent_of_market_volatility():
    option, market, model = _make_setup()
    target = model.price(option, market)
    input_market = market.with_volatility(0.0)

    implied_vol = ImpliedVolatility(model).solve(
        option,
        input_market,
        target,
        method="newton",
        initial_guess=0.4,
    )

    assert abs(implied_vol - 0.2) < 1e-4


def test_bisection_default_tolerances_control_repricing_error():
    option = EuropeanOption(strike=50, maturity=1, option_type="call")
    market = MarketData(spot=50, rate=-0.02, volatility=0.1)
    model = BlackScholes()
    target = model.price(option, market)

    implied_vol = ImpliedVolatility(model).solve(
        option,
        market.with_volatility(0.0),
        target,
        method=RootFindingMethod.BISECTION,
    )

    repriced = model.price(option, market.with_volatility(implied_vol))
    assert abs(repriced - target) <= 1e-6


def test_legacy_tol_remains_supported():
    option, market, model = _make_setup()
    target = model.price(option, market)

    implied_vol = ImpliedVolatility(model).solve(
        option, market, target, method="bisection", tol=1e-6
    )

    assert abs(implied_vol - 0.2) < 1e-4


@pytest.mark.parametrize("name", ["vol_tol", "price_tol"])
def test_invalid_separate_tolerance_is_rejected(name):
    option, market, model = _make_setup()
    target = model.price(option, market)

    with pytest.raises(ValueError, match="vol_tol and price_tol"):
        ImpliedVolatility(model).solve(option, market, target, **{name: 0.0})
