from enum import Enum


class OptionType(str, Enum):
    CALL = "call"
    PUT = "put"


class RootFindingMethod(str, Enum):
    BRENT = "brent"
    BISECTION = "bisection"
    NEWTON = "newton"
