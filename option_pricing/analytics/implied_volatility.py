import math
from numbers import Real

from option_pricing.analytical import BlackScholes
from option_pricing.common import (
    ConvergenceError,
    MarketData,
    OptionType,
    RootFindingMethod,
)
from option_pricing.numerical import find_root
from option_pricing.products import EuropeanOption


class ImpliedVolatility:
    """Recover Black-Scholes volatility from a European option price."""

    def __init__(self, model: BlackScholes):
        self.model = model

    def solve(
        self,
        option: EuropeanOption,
        market: MarketData,
        target_price: float,
        method: RootFindingMethod | str = RootFindingMethod.BRENT,
        tol: float | None = None,
        max_iter: int = 200,
        min_vol: float = 1e-8,
        max_vol: float = 5.0,
        max_vol_limit: float = 100.0,
        initial_guess: float = 0.2,
        vol_tol: float | None = None,
        price_tol: float | None = None,
    ) -> float:
        """Return the volatility whose model price matches ``target_price``.

        ``max_vol`` is an initial bracket, not a hard volatility ceiling. It is
        expanded up to ``max_vol_limit`` when the target has a finite solution.
        Newton's method is safeguarded by the same bracket and falls back to a
        bisection step whenever its derivative is too small or its step escapes.

        ``vol_tol`` controls root accuracy in volatility units and ``price_tol``
        controls the repricing residual. The legacy ``tol`` argument remains
        supported: when supplied, it provides the default for either new
        tolerance that was not explicitly set. ``initial_guess`` is used only by
        Newton's method; the volatility already present in ``market`` is ignored.
        """
        selected_method = self._validate_method(method)
        vol_tol, price_tol = self._resolve_tolerances(tol, vol_tol, price_tol)
        self._validate_inputs(
            target_price,
            vol_tol,
            price_tol,
            max_iter,
            min_vol,
            max_vol,
            max_vol_limit,
            initial_guess,
        )
        lower_price, upper_price = self._arbitrage_bounds(option, market)
        if target_price < lower_price - price_tol or target_price >= upper_price:
            raise ValueError(
                f"target_price must be in [{lower_price}, {upper_price})."
            )
        if abs(target_price - lower_price) <= price_tol:
            return 0.0

        def price_error(volatility: float) -> float:
            return self._price_with_vol(option, market, volatility) - target_price

        low = min_vol
        if price_error(low) >= 0:
            return 0.0

        high = max_vol
        while price_error(high) < 0 and high < max_vol_limit:
            high = min(2 * high, max_vol_limit)
        if price_error(high) < 0:
            raise ConvergenceError(
                "Could not bracket implied volatility before max_vol_limit."
            )

        result = find_root(
            price_error,
            bracket=(low, high),
            method=selected_method,
            derivative=lambda volatility: self._vega_with_vol(
                option, market, volatility
            ),
            initial_guess=initial_guess,
            x_tol=self._effective_vol_tolerance(option, market, vol_tol, price_tol),
            f_tol=price_tol,
            max_iter=max_iter,
        )
        if result.residual > price_tol:
            raise ConvergenceError(
                "Implied volatility met vol_tol but not price_tol; "
                "use a smaller vol_tol."
            )
        return result.root

    @staticmethod
    def _effective_vol_tolerance(
        option: EuropeanOption,
        market: MarketData,
        vol_tol: float,
        price_tol: float,
    ) -> float:
        max_vega = market.spot * math.sqrt(option.maturity) / math.sqrt(2 * math.pi)
        price_implied_vol_tol = 0.5 * price_tol / max_vega
        return min(vol_tol, price_implied_vol_tol)

    def _price_with_vol(
        self,
        option: EuropeanOption,
        market: MarketData,
        volatility: float,
    ) -> float:
        return self.model.price(option, market.with_volatility(volatility))

    def _vega_with_vol(
        self,
        option: EuropeanOption,
        market: MarketData,
        volatility: float,
    ) -> float:
        return self.model.vega(option, market.with_volatility(volatility))

    @staticmethod
    def _arbitrage_bounds(
        option: EuropeanOption, market: MarketData
    ) -> tuple[float, float]:
        discounted_strike = option.strike * math.exp(
            -market.rate * option.maturity
        )
        if option.option_type is OptionType.CALL:
            return max(0.0, market.spot - discounted_strike), market.spot
        return max(0.0, discounted_strike - market.spot), discounted_strike

    @staticmethod
    def _validate_method(method: RootFindingMethod | str) -> RootFindingMethod:
        try:
            return RootFindingMethod(method)
        except (TypeError, ValueError) as exc:
            raise ValueError(f"Unknown root-finding method: {method}") from exc

    @staticmethod
    def _resolve_tolerances(
        tol: float | None,
        vol_tol: float | None,
        price_tol: float | None,
    ) -> tuple[float, float]:
        resolved_vol_tol = vol_tol
        if resolved_vol_tol is None:
            resolved_vol_tol = tol if tol is not None else 1e-8

        resolved_price_tol = price_tol
        if resolved_price_tol is None:
            resolved_price_tol = tol if tol is not None else 1e-6

        return resolved_vol_tol, resolved_price_tol

    @staticmethod
    def _validate_inputs(
        target_price: float,
        vol_tol: float,
        price_tol: float,
        max_iter: int,
        min_vol: float,
        max_vol: float,
        max_vol_limit: float,
        initial_guess: float,
    ) -> None:
        for name, value in (
            ("target_price", target_price),
            ("vol_tol", vol_tol),
            ("price_tol", price_tol),
            ("min_vol", min_vol),
            ("max_vol", max_vol),
            ("max_vol_limit", max_vol_limit),
            ("initial_guess", initial_guess),
        ):
            if (
                isinstance(value, bool)
                or not isinstance(value, Real)
                or not math.isfinite(value)
            ):
                raise ValueError(f"{name} must be a finite real number.")
        if target_price < 0:
            raise ValueError("target_price cannot be negative.")
        if vol_tol <= 0 or price_tol <= 0:
            raise ValueError("vol_tol and price_tol must be positive.")
        if not isinstance(max_iter, int) or isinstance(max_iter, bool) or max_iter <= 0:
            raise ValueError("max_iter must be a positive integer.")
        if not 0 < min_vol < max_vol <= max_vol_limit:
            raise ValueError(
                "volatility bounds must satisfy "
                "0 < min_vol < max_vol <= max_vol_limit."
            )
        if initial_guess <= 0:
            raise ValueError("initial_guess must be positive.")
