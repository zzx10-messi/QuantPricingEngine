import numpy as np
from scipy.stats import norm

from src.instruments.option import EuropeanOption
from src.market.data import MarketData
from src.models.base import PricingModel


class BlackScholes(PricingModel):
    """
    Black-Scholes pricing model for European options.
    """

    def price(self, option: EuropeanOption, market: MarketData) -> float:
        """
        Calculate the theoretical price of a European option.
        """
        d1 = self._calculate_d1(option, market)
        d2 = self._calculate_d2(d1, market, option)

        discount_factor = np.exp(-market.rate * option.maturity)

        if option.option_type == "call":
            return market.spot * norm.cdf(d1) - option.strike * discount_factor * norm.cdf(d2)
        elif option.option_type == "put":
            return option.strike * discount_factor * norm.cdf(-d2) - market.spot * norm.cdf(-d1)

    def _calculate_d1(
        self,
        option: EuropeanOption,
        market: MarketData,
    ) -> float:
        """Calculate d1 for the Black-Scholes formula."""
        return (
            np.log(market.spot / option.strike)
            + (market.rate + 0.5 * market.volatility**2) * option.maturity
        ) / (market.volatility * np.sqrt(option.maturity))

    def _calculate_d2(
        self,
        d1: float,
        market: MarketData,
        option: EuropeanOption,
    ) -> float:
        """Calculate d2 for the Black-Scholes formula."""
        return d1 - market.volatility * np.sqrt(option.maturity)
