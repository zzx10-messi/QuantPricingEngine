import math

from option_pricing.analytical import BlackScholes
from option_pricing.common import ConvergenceError, MarketData, OptionType
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
        method: str = "brent",
        tol: float = 1e-6,
        max_iter: int = 200,
        min_vol: float = 1e-8,
        max_vol: float = 5.0,
        max_vol_limit: float = 100.0,
    ) -> float:
        """Return the volatility whose model price matches ``target_price``.

        ``max_vol`` is an initial bracket, not a hard volatility ceiling. It is
        expanded up to ``max_vol_limit`` when the target has a finite solution.
        Newton's method is safeguarded by the same bracket and falls back to a
        bisection step whenever its derivative is too small or its step escapes.
        """
        self._validate_inputs(
            option, market, target_price, tol, max_iter, min_vol, max_vol,
            max_vol_limit
        )
        lower_price, upper_price = self._arbitrage_bounds(option, market)
        if target_price < lower_price - tol or target_price >= upper_price:
            raise ValueError(
                f"target_price must be in [{lower_price}, {upper_price})."
            )
        if abs(target_price - lower_price) <= tol:
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
            method=method,
            derivative=lambda volatility: self._vega_with_vol(
                option, market, volatility
            ),
            initial_guess=market.volatility,
            x_tol=tol,
            f_tol=tol,
            max_iter=max_iter,
        )
        return result.root

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
    def _validate_inputs(
        option: EuropeanOption,
        market: MarketData,
        target_price: float,
        tol: float,
        max_iter: int,
        min_vol: float,
        max_vol: float,
        max_vol_limit: float,
    ) -> None:
        del option, market
        for name, value in (
            ("target_price", target_price),
            ("tol", tol),
            ("min_vol", min_vol),
            ("max_vol", max_vol),
            ("max_vol_limit", max_vol_limit),
        ):
            if not isinstance(value, (int, float)) or not math.isfinite(value):
                raise ValueError(f"{name} must be a finite real number.")
        if target_price < 0:
            raise ValueError("target_price cannot be negative.")
        if tol <= 0:
            raise ValueError("tol must be positive.")
        if not isinstance(max_iter, int) or isinstance(max_iter, bool) or max_iter <= 0:
            raise ValueError("max_iter must be a positive integer.")
        if not 0 < min_vol < max_vol <= max_vol_limit:
            raise ValueError(
                "volatility bounds must satisfy "
                "0 < min_vol < max_vol <= max_vol_limit."
            )
