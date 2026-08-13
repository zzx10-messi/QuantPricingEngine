from dataclasses import dataclass


@dataclass(frozen=True)
class EuropeanOption:
    """
    European option contract.

    Parameters
    ----------
    strike : float
        Strike price K.
    maturity : float
        Time to maturity in years.
    option_type : str
        Option type: 'call' or 'put'.
    """

    strike: float
    maturity: float
    option_type: str

    def __post_init__(self):
        if self.strike <= 0:
            raise ValueError("Strike price must be positive.")

        if self.maturity <= 0:
            raise ValueError("Maturity must be positive.")

        if self.option_type not in {"call", "put"}:
            raise ValueError("Option type must be 'call' or 'put'.")
