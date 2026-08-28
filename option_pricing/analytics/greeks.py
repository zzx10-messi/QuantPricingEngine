import numpy as np
from scipy.stats import norm

from option_pricing.analytical import BlackScholes
from option_pricing.common import MarketData, OptionType
from option_pricing.products import EuropeanOption


class Greeks:
    """Analytical Black-Scholes Greeks."""

    def __init__(self, model: BlackScholes):
        self.model = model

    def _d1_d2(
        self, option: EuropeanOption, market: MarketData
    ) -> tuple[float, float]:
        d1 = self.model.d1(option, market)
        return d1, self.model.d2(option, market, d1=d1)

    def delta(self, option: EuropeanOption, market: MarketData) -> float:
        d1, _ = self._d1_d2(option, market)
        if option.option_type is OptionType.CALL:
            return float(norm.cdf(d1))
        return float(norm.cdf(d1) - 1)

    def gamma(self, option: EuropeanOption, market: MarketData) -> float:
        d1, _ = self._d1_d2(option, market)
        return float(
            norm.pdf(d1)
            / (market.spot * market.volatility * np.sqrt(option.maturity))
        )

    def vega(self, option: EuropeanOption, market: MarketData) -> float:
        return self.model.vega(option, market)

    def theta(self, option: EuropeanOption, market: MarketData) -> float:
        d1, d2 = self._d1_d2(option, market)
        diffusion = -(
            market.spot * norm.pdf(d1) * market.volatility
        ) / (2 * np.sqrt(option.maturity))
        discounted_strike = option.strike * np.exp(-market.rate * option.maturity)
        if option.option_type is OptionType.CALL:
            carry = -market.rate * discounted_strike * norm.cdf(d2)
        else:
            carry = market.rate * discounted_strike * norm.cdf(-d2)
        return float(diffusion + carry)

    def rho(self, option: EuropeanOption, market: MarketData) -> float:
        _, d2 = self._d1_d2(option, market)
        discounted_strike = option.strike * np.exp(-market.rate * option.maturity)
        if option.option_type is OptionType.CALL:
            return float(option.maturity * discounted_strike * norm.cdf(d2))
        return float(-option.maturity * discounted_strike * norm.cdf(-d2))
