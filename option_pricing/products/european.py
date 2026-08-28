from dataclasses import dataclass

from option_pricing.common.enums import OptionType
from option_pricing.common.validation import validate_positive


@dataclass(frozen=True)
class EuropeanOption:
    """A vanilla European option contract."""

    strike: float
    maturity: float
    option_type: OptionType | str

    def __post_init__(self) -> None:
        validate_positive("strike", self.strike)
        validate_positive("maturity", self.maturity)
        try:
            option_type = OptionType(self.option_type)
        except ValueError as exc:
            raise ValueError("option_type must be 'call' or 'put'.") from exc
        object.__setattr__(self, "option_type", option_type)
