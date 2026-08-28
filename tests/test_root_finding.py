import pytest

from option_pricing.common import ConvergenceError, RootFindingMethod
from option_pricing.numerical import find_root


@pytest.mark.parametrize("method", ["brent", "bisection", "newton"])
def test_root_finding_methods(method):
    result = find_root(
        lambda x: x * x - 2,
        derivative=lambda x: 2 * x,
        bracket=(0.0, 2.0),
        initial_guess=1.0,
        method=method,
    )

    assert abs(result.root - 2**0.5) < 1e-5
    assert result.residual < 1e-5
    assert result.method == method


def test_invalid_method_is_rejected_before_endpoint_return():
    with pytest.raises(ValueError, match="Unknown root-finding method"):
        find_root(lambda x: x, bracket=(0.0, 1.0), method="foo")


def test_newton_requires_derivative_even_when_root_is_at_endpoint():
    with pytest.raises(ValueError, match="requires a derivative"):
        find_root(lambda x: x, bracket=(0.0, 1.0), method="newton")


@pytest.mark.parametrize("method", ["brent", "bisection", "newton"])
def test_non_finite_function_value_is_rejected(method):
    with pytest.raises(ValueError, match="non-finite"):
        find_root(
            lambda x: float("nan"),
            derivative=lambda x: 1.0,
            bracket=(0.0, 1.0),
            method=method,
        )


def test_non_finite_newton_derivative_is_rejected():
    with pytest.raises(ValueError, match="derivative returned a non-finite"):
        find_root(
            lambda x: x - 0.5,
            derivative=lambda x: float("nan"),
            bracket=(0.0, 1.0),
            initial_guess=0.25,
            method="newton",
        )


def test_brent_uses_convergence_error():
    with pytest.raises(ConvergenceError):
        find_root(
            lambda x: x * x - 2,
            bracket=(0.0, 2.0),
            method="brent",
            max_iter=1,
        )


def test_unbracketed_root_is_rejected():
    with pytest.raises(ValueError, match="not bracketed"):
        find_root(lambda x: x * x + 1, bracket=(-1.0, 1.0))


def test_method_enum_is_supported():
    result = find_root(
        lambda x: x - 0.5,
        bracket=(0.0, 1.0),
        method=RootFindingMethod.BRENT,
    )

    assert result.root == 0.5
    assert result.method == "brent"
