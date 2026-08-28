import pytest

from option_pricing.common import OptionType
from option_pricing.products import EuropeanOption


def test_create_call_option():
    option = EuropeanOption(
        strike=100,
        maturity=1,
        option_type="call",
    )

    assert option.strike == 100
    assert option.maturity == 1
    assert option.option_type is OptionType.CALL


def test_create_put_option():
    option = EuropeanOption(
        strike=100,
        maturity=1,
        option_type="put",
    )
    assert option.strike == 100
    assert option.maturity == 1
    assert option.option_type is OptionType.PUT


def test_invalid_strike():
    with pytest.raises(ValueError):
        EuropeanOption(
            strike=-100,
            maturity=1,
            option_type="call",
        )


def test_invalid_maturity():
    with pytest.raises(ValueError):
        EuropeanOption(
            strike=100,
            maturity=0,
            option_type="call",
        )


def test_invalid_option_type():
    with pytest.raises(ValueError):
        EuropeanOption(
            strike=100,
            maturity=1,
            option_type="straddle",
        )


def test_non_string_option_type_is_rejected_consistently():
    with pytest.raises(ValueError, match="option_type"):
        EuropeanOption(strike=100, maturity=1, option_type=None)


@pytest.mark.parametrize("field", ["strike", "maturity"])
def test_boolean_contract_inputs_are_rejected(field):
    values = {"strike": 100, "maturity": 1, "option_type": "call"}
    values[field] = True
    with pytest.raises(ValueError):
        EuropeanOption(**values)
