from dataclasses import dataclass


@dataclass(frozen=True)
class RootFindingResult:
    """Diagnostics returned by a numerical root finder."""

    root: float
    iterations: int
    residual: float
    method: str
