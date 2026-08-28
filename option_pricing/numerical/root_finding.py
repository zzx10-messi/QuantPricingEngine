from collections.abc import Callable

from scipy.optimize import brentq

from option_pricing.common import ConvergenceError, RootFindingResult


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
    if x_tol <= 0 or f_tol <= 0:
        raise ValueError("x_tol and f_tol must be positive.")
    if max_iter <= 0:
        raise ValueError("max_iter must be positive.")

    low, high = bracket
    if not low < high:
        raise ValueError("bracket must satisfy low < high.")
    f_low, f_high = function(low), function(high)
    if f_low == 0:
        return RootFindingResult(low, 0, 0.0, method)
    if f_high == 0:
        return RootFindingResult(high, 0, 0.0, method)
    if f_low * f_high > 0:
        raise ValueError("The root is not bracketed.")

    if method == "brent":
        root, details = brentq(
            function, low, high, xtol=x_tol, maxiter=max_iter, full_output=True
        )
        if not details.converged:
            raise ConvergenceError("Brent's method did not converge.")
        return RootFindingResult(
            float(root), details.iterations, abs(function(root)), method
        )
    if method == "bisection":
        return _bisection(function, low, high, f_low, x_tol, f_tol, max_iter)
    if method == "newton":
        if derivative is None:
            raise ValueError("Newton's method requires a derivative.")
        guess = (low + high) / 2 if initial_guess is None else initial_guess
        return _safeguarded_newton(
            function, derivative, low, high, f_low, guess, x_tol, f_tol, max_iter
        )
    raise ValueError(f"Unknown root-finding method: {method}")


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
        if abs(f_mid) <= f_tol or (high - low) / 2 <= x_tol:
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
