import numpy as np
from scipy.stats import norm

from option_pricing.common import MarketData, OptionType
from option_pricing.products import EuropeanOption


class BlackScholes:
    """Black-Scholes analytical pricer for vanilla European options.

    At zero volatility, :meth:`price` returns the discounted deterministic
    payoff. Distribution parameters and analytical sensitivities that depend on
    them remain undefined at that boundary.
    """

    def price(self, option: EuropeanOption, market: MarketData) -> float:
        if market.volatility == 0:
            return self._zero_volatility_price(option, market)

        d1 = self.d1(option, market)
        d2 = self.d2(option, market, d1=d1)
        discounted_strike = option.strike * np.exp(-market.rate * option.maturity)

        if option.option_type is OptionType.CALL:
            return float(market.spot * norm.cdf(d1) - discounted_strike * norm.cdf(d2))
        return float(discounted_strike * norm.cdf(-d2) - market.spot * norm.cdf(-d1))

    def d1(self, option: EuropeanOption, market: MarketData) -> float:
        if market.volatility == 0:
            raise ValueError("d1 is undefined when volatility is zero.")
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
        if market.volatility == 0:
            raise ValueError("d2 is undefined when volatility is zero.")
        d1 = self.d1(option, market) if d1 is None else d1
        return float(d1 - market.volatility * np.sqrt(option.maturity))

    def vega(self, option: EuropeanOption, market: MarketData) -> float:
        if market.volatility == 0:
            raise ValueError("vega is undefined when volatility is zero.")
        return float(
            market.spot * norm.pdf(self.d1(option, market)) * np.sqrt(option.maturity)
        )

    @staticmethod
    def _zero_volatility_price(
        option: EuropeanOption, market: MarketData
    ) -> float:
        discounted_strike = option.strike * np.exp(-market.rate * option.maturity)
        if option.option_type is OptionType.CALL:
            return float(max(market.spot - discounted_strike, 0.0))
        return float(max(discounted_strike - market.spot, 0.0))
