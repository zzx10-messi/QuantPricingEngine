import pytest

from src.instruments import EuropeanOption



def test_create_call_option():

    option = EuropeanOption(
        strike=100,
        maturity=1,
        option_type="call"
    )


    assert option.strike == 100

    assert option.maturity == 1

    assert option.option_type == "call"



def test_invalid_strike():

    with pytest.raises(
        ValueError
    ):

        EuropeanOption(
            strike=-100,
            maturity=1,
            option_type="call"
        )