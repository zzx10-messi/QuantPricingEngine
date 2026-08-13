from dataclasses import dataclass


@dataclass(frozen=True)
class MarketData:
    """
    Market environment required for pricing.

    Parameters
    ----------
    spot : float
        Current underlying asset price S0.
    rate : float
        Risk-free interest rate r.
    volatility : float
        Volatility sigma.
    """

    spot: float
    rate: float
    volatility: float

    def __post_init__(self):
        if self.spot <= 0:
            raise ValueError("Spot price must be positive.")

        if self.rate < 0:
            raise ValueError("Interest rate cannot be negative.")

        if self.volatility <= 0:
            raise ValueError("Volatility must be positive.")
