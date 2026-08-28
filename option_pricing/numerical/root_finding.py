from collections.abc import Callable
import math
from numbers import Real

from scipy.optimize import brentq

from option_pricing.common import (
    ConvergenceError,
    RootFindingMethod,
    RootFindingResult,
)


ScalarFunction = Callable[[float], float]


def find_root(
    function: ScalarFunction,
    *,
    bracket: tuple[float, float],
    method: str = "brent",
    derivative: ScalarFunction | None = None,
    initial_guess: float | None = None,
    x_tol: float = 1e-6,
    f_tol: float = 1e-6,
    max_iter: int = 200,
) -> RootFindingResult:
    """Find a scalar root using a bracketed, convergence-checked method."""
    try:
        selected_method = RootFindingMethod(method)
    except (TypeError, ValueError) as exc:
        raise ValueError(f"Unknown root-finding method: {method}") from exc
    if selected_method is RootFindingMethod.NEWTON and derivative is None:
        raise ValueError("Newton's method requires a derivative.")
    if initial_guess is not None and not _is_finite_real(initial_guess):
        raise ValueError("initial_guess must be a finite real number.")
    if not _is_finite_real(x_tol) or not _is_finite_real(f_tol):
        raise ValueError("x_tol and f_tol must be finite real numbers.")
    if x_tol <= 0 or f_tol <= 0:
        raise ValueError("x_tol and f_tol must be positive.")
    if not isinstance(max_iter, int) or isinstance(max_iter, bool) or max_iter <= 0:
        raise ValueError("max_iter must be a positive integer.")

    low, high = bracket
    if not _is_finite_real(low) or not _is_finite_real(high):
        raise ValueError("bracket endpoints must be finite real numbers.")
    if not low < high:
        raise ValueError("bracket must satisfy low < high.")
    checked_function = _checked(function, "function")
    f_low, f_high = checked_function(low), checked_function(high)
    if f_low == 0:
        return RootFindingResult(float(low), 0, 0.0, selected_method.value)
    if f_high == 0:
        return RootFindingResult(float(high), 0, 0.0, selected_method.value)
    if f_low * f_high > 0:
        raise ValueError("The root is not bracketed.")

    if selected_method is RootFindingMethod.BRENT:
        root, details = brentq(
            checked_function,
            low,
            high,
            xtol=x_tol,
            maxiter=max_iter,
            full_output=True,
            disp=False,
        )
        if not details.converged:
            raise ConvergenceError("Brent's method did not converge.")
        residual = abs(checked_function(root))
        if residual > f_tol:
            raise ConvergenceError(
                "Brent's method met x_tol but not f_tol; use a smaller x_tol."
            )
        return RootFindingResult(
            float(root), details.iterations, residual, selected_method.value
        )
    if selected_method is RootFindingMethod.BISECTION:
        return _bisection(
            checked_function, low, high, f_low, x_tol, f_tol, max_iter
        )

    assert derivative is not None
    checked_derivative = _checked(derivative, "derivative")
    guess = (low + high) / 2 if initial_guess is None else initial_guess
    return _safeguarded_newton(
        checked_function,
        checked_derivative,
        low,
        high,
        f_low,
        guess,
        x_tol,
        f_tol,
        max_iter,
    )


def _is_finite_real(value: object) -> bool:
    return (
        not isinstance(value, bool)
        and isinstance(value, Real)
        and math.isfinite(value)
    )


def _checked(function: ScalarFunction, name: str) -> ScalarFunction:
    def evaluate(value: float) -> float:
        result = function(value)
        if not _is_finite_real(result):
            raise ValueError(f"{name} returned a non-finite real value at x={value}.")
        return float(result)

    return evaluate


def _bisection(
    function: ScalarFunction,
    low: float,
    high: float,
    f_low: float,
    x_tol: float,
    f_tol: float,
    max_iter: int,
) -> RootFindingResult:
    for iteration in range(1, max_iter + 1):
        mid = (low + high) / 2
        f_mid = function(mid)
        if abs(f_mid) <= f_tol and (high - low) / 2 <= x_tol:
            return RootFindingResult(mid, iteration, abs(f_mid), "bisection")
        if f_low * f_mid < 0:
            high = mid
        else:
            low, f_low = mid, f_mid
    raise ConvergenceError("Bisection did not converge within max_iter.")


def _safeguarded_newton(
    function: ScalarFunction,
    derivative: ScalarFunction,
    low: float,
    high: float,
    f_low: float,
    guess: float,
    x_tol: float,
    f_tol: float,
    max_iter: int,
) -> RootFindingResult:
    current = guess if low < guess < high else (low + high) / 2
    for iteration in range(1, max_iter + 1):
        value = function(current)
        if abs(value) <= f_tol:
            return RootFindingResult(current, iteration, abs(value), "newton")

        if f_low * value < 0:
            high = current
        else:
            low, f_low = current, value

        slope = derivative(current)
        candidate = current - value / slope if abs(slope) > 1e-14 else float("nan")
        if not low < candidate < high:
            candidate = (low + high) / 2
        if abs(candidate - current) <= x_tol:
            residual = abs(function(candidate))
            if residual <= f_tol:
                return RootFindingResult(candidate, iteration, residual, "newton")
        current = candidate
    raise ConvergenceError("Newton's method did not converge within max_iter.")
