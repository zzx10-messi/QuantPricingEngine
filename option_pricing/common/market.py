from dataclasses import dataclass, replace

from option_pricing.common.validation import validate_finite, validate_positive


@dataclass(frozen=True)
class MarketData:
    """Market inputs used by the currently implemented pricing models."""

    spot: float
    rate: float
    volatility: float

    def __post_init__(self) -> None:
        validate_positive("spot", self.spot)
        validate_finite("rate", self.rate)
        validate_positive("volatility", self.volatility)

    def with_volatility(self, volatility: float) -> "MarketData":
        return replace(self, volatility=volatility)
