import math
from numbers import Real


def validate_finite(name: str, value: object) -> Real:
    if isinstance(value, bool) or not isinstance(value, Real) or not math.isfinite(value):
        raise ValueError(f"{name} must be a finite real number.")
    return value


def validate_positive(name: str, value: object) -> None:
    finite_value = validate_finite(name, value)
    if finite_value <= 0:
        raise ValueError(f"{name} must be positive.")


def validate_nonnegative(name: str, value: object) -> None:
    finite_value = validate_finite(name, value)
    if finite_value < 0:
        raise ValueError(f"{name} cannot be negative.")
