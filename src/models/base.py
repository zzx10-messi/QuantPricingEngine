from abc import ABC, abstractmethod

from src.instruments.option import EuropeanOption
from src.market.data import MarketData


class PricingModel(ABC):
    """
    Abstract base class for pricing models.
    """

    @abstractmethod
    def price(self, option: EuropeanOption, market: MarketData) -> float:
        """
        Calculate the theoretical price of an option.

        Must be implemented by subclasses.
        """
        ...
