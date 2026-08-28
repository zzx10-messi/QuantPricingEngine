import numpy as np
from scipy.stats import norm

from option_pricing.common import MarketData, OptionType
from option_pricing.products import EuropeanOption


class BlackScholes:
    """Black-Scholes analytical pricer for vanilla European options."""

    def price(self, option: EuropeanOption, market: MarketData) -> float:
        d1 = self.d1(option, market)
        d2 = self.d2(option, market, d1=d1)
        discounted_strike = option.strike * np.exp(-market.rate * option.maturity)

        if option.option_type is OptionType.CALL:
            return float(market.spot * norm.cdf(d1) - discounted_strike * norm.cdf(d2))
        return float(discounted_strike * norm.cdf(-d2) - market.spot * norm.cdf(-d1))

    def d1(self, option: EuropeanOption, market: MarketData) -> float:
        numerator = np.log(market.spot / option.strike) + (
            market.rate + 0.5 * market.volatility**2
        ) * option.maturity
        return float(numerator / (market.volatility * np.sqrt(option.maturity)))

    def d2(
        self,
        option: EuropeanOption,
        market: MarketData,
        *,
        d1: float | None = None,
    ) -> float:
        d1 = self.d1(option, market) if d1 is None else d1
        return float(d1 - market.volatility * np.sqrt(option.maturity))

    def vega(self, option: EuropeanOption, market: MarketData) -> float:
        return float(
            market.spot * norm.pdf(self.d1(option, market)) * np.sqrt(option.maturity)
        )
