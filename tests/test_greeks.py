from src.instruments import EuropeanOption
from src.market import MarketData
from src.models import BlackScholes
from src.risk import Greeks



def test_call_greeks():

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


    greeks = Greeks(
        model
    )


    delta = greeks.delta(
        option,
        market
    )


    gamma = greeks.gamma(
        option,
        market
    )


    vega = greeks.vega(
        option,
        market
    )


    theta = greeks.theta(
        option,
        market
    )


    rho = greeks.rho(
        option,
        market
    )



    assert abs(
        delta - 0.636831
    ) < 1e-5



    assert abs(
        gamma - 0.018762
    ) < 1e-5



    assert abs(
        vega - 37.524035
    ) < 1e-5



    assert abs(
        theta - (-6.414028)
    ) < 1e-5



    assert abs(
        rho - 53.232482
    ) < 1e-5