import math
from numbers import Real


def validate_finite(name: str, value: Real) -> None:
    if not isinstance(value, Real) or not math.isfinite(value):
        raise ValueError(f"{name} must be a finite real number.")


def validate_positive(name: str, value: Real) -> None:
    validate_finite(name, value)
    if value <= 0:
        raise ValueError(f"{name} must be positive.")
