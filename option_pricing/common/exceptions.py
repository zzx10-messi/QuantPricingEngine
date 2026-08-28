class PricingEngineError(Exception):
    """Base exception for the option pricing package."""


class ConvergenceError(PricingEngineError, ValueError):
    """Raised when a numerical method cannot produce a reliable result."""
