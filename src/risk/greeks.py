import numpy as np
from scipy.stats import norm

from src.instruments.option import EuropeanOption
from src.market.data import MarketData
from src.models.black_scholes import BlackScholes


class Greeks:
    """
    Calculate option risk sensitivities.

    Supported Greeks:
    - Delta
    - Gamma
    - Vega
    - Theta
    - Rho

    Currently based on Black-Scholes analytical formulas.
    """

    def __init__(
        self,
        model: BlackScholes
    ):
        """
        Parameters
        ----------
        model : BlackScholes
            Pricing model used for Greek calculation.
        """

        self.model = model


    def _calculate_d1_d2(
        self,
        option: EuropeanOption,
        market: MarketData
    ) -> tuple[float, float]:
        """
        Calculate d1 and d2.

        Returns
        -------
        tuple
            (d1, d2)
        """

        d1 = self.model._calculate_d1(
            option,
            market
        )

        d2 = self.model._calculate_d2(
            d1,
            market,
            option
        )

        return d1, d2



    def delta(
        self,
        option: EuropeanOption,
        market: MarketData
    ) -> float:
        """
        Calculate Delta.

        Delta = ∂V / ∂S

        Measures sensitivity to underlying price.
        """

        d1, _ = self._calculate_d1_d2(
            option,
            market
        )


        if option.option_type == "call":

            return norm.cdf(d1)


        else:

            return norm.cdf(d1) - 1



    def gamma(
        self,
        option: EuropeanOption,
        market: MarketData
    ) -> float:
        """
        Calculate Gamma.

        Gamma = ∂²V / ∂S²

        Measures Delta change speed.
        """

        d1, _ = self._calculate_d1_d2(
            option,
            market
        )


        return (
            norm.pdf(d1)
            /
            (
                market.spot
                *
                market.volatility
                *
                np.sqrt(option.maturity)
            )
        )



    def vega(
        self,
        option: EuropeanOption,
        market: MarketData
    ) -> float:
        """
        Calculate Vega.

        Vega = ∂V / ∂σ

        Measures volatility sensitivity.

        Note:
        Usually interpreted per 1% volatility change.
        """

        d1, _ = self._calculate_d1_d2(
            option,
            market
        )


        return (
            market.spot
            *
            norm.pdf(d1)
            *
            np.sqrt(option.maturity)
        )



    def theta(
        self,
        option: EuropeanOption,
        market: MarketData
    ) -> float:
        """
        Calculate Theta.

        Theta = ∂V / ∂t

        Measures time decay.
        """

        d1, d2 = self._calculate_d1_d2(
            option,
            market
        )


        first_term = (
            -
            (
                market.spot
                *
                norm.pdf(d1)
                *
                market.volatility
            )
            /
            (
                2
                *
                np.sqrt(option.maturity)
            )
        )


        discount_factor = np.exp(
            -market.rate
            *
            option.maturity
        )


        if option.option_type == "call":

            second_term = (
                -
                market.rate
                *
                option.strike
                *
                discount_factor
                *
                norm.cdf(d2)
            )


        else:

            second_term = (
                market.rate
                *
                option.strike
                *
                discount_factor
                *
                norm.cdf(-d2)
            )


        return first_term + second_term



    def rho(
        self,
        option: EuropeanOption,
        market: MarketData
    ) -> float:
        """
        Calculate Rho.

        Rho = ∂V / ∂r

        Measures interest rate sensitivity.
        """

        _, d2 = self._calculate_d1_d2(
            option,
            market
        )


        discount_factor = np.exp(
            -market.rate
            *
            option.maturity
        )


        if option.option_type == "call":

            return (
                option.strike
                *
                option.maturity
                *
                discount_factor
                *
                norm.cdf(d2)
            )


        else:

            return (
                -
                option.strike
                *
                option.maturity
                *
                discount_factor
                *
                norm.cdf(-d2)
            )