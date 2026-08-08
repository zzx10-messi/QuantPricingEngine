from src.instruments import EuropeanOption
from src.market import MarketData
from src.models import BlackScholes



def test_european_call_price():

    option = EuropeanOption(
        strike=100,
        maturity=1,
        option_type="call"
    )


    market = MarketData(
        spot=100,
        rate=0.05,
        volatility=0.2
    )


    model = BlackScholes()


    price = model.price(
        option,
        market
    )


    expected_price = 10.450584


    assert abs(
        price - expected_price
    ) < 1e-5