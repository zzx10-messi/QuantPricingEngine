import numpy as np
from scipy.stats import norm


from src.models.base import PricingModel
from src.instruments.option import EuropeanOption
from src.market.data import MarketData



class BlackScholes(PricingModel):
    """
    Black-Scholes pricing model
    for European options.
    """



    def price(
        self,
        option: EuropeanOption,
        market: MarketData
    ) -> float:
        """
        Calculate option theoretical price.
        """


        d1 = self._calculate_d1(
            option,
            market
        )


        d2 = self._calculate_d2(
            d1,
            market,
            option
        )



        if option.option_type == "call":

            return (
                market.spot
                *
                norm.cdf(d1)

                -

                option.strike
                *
                np.exp(
                    -market.rate
                    *
                    option.maturity
                )
                *
                norm.cdf(d2)
            )


        else:

            return (
                option.strike
                *
                np.exp(
                    -market.rate
                    *
                    option.maturity
                )
                *
                norm.cdf(-d2)

                -

                market.spot
                *
                norm.cdf(-d1)
            )



    def _calculate_d1(
        self,
        option: EuropeanOption,
        market: MarketData
    ) -> float:


        return (
            np.log(
                market.spot
                /
                option.strike
            )

            +

            (
                market.rate
                +
                0.5
                *
                market.volatility**2
            )
            *
            option.maturity

        ) / (

            market.volatility
            *
            np.sqrt(
                option.maturity
            )

        )



    def _calculate_d2(
        self,
        d1: float,
        market: MarketData,
        option: EuropeanOption
    ) -> float:


        return (
            d1
            -
            market.volatility
            *
            np.sqrt(
                option.maturity
            )
        )