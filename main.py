from option_pricing.analytical import BlackScholes
from option_pricing.analytics import Greeks
from option_pricing.common import MarketData
from option_pricing.products import EuropeanOption


def main():
    # Create European call option
    option = EuropeanOption(
        strike=100,
        maturity=1,
        option_type="call",
    )

    # Create market environment
    market = MarketData(
        spot=100,
        rate=0.05,
        volatility=0.2,
    )

    # Create pricing model
    model = BlackScholes()

    # Calculate price and Greeks
    price = model.price(option, market)

    greeks = Greeks(model)
    delta = greeks.delta(option, market)
    gamma = greeks.gamma(option, market)
    vega = greeks.vega(option, market)
    theta = greeks.theta(option, market)
    rho = greeks.rho(option, market)

    print("=" * 40)
    print("European Call Option")
    print("=" * 40)
    print(f"Price: {price:.6f}")
    print(f"Delta: {delta:.6f}")
    print(f"Gamma: {gamma:.6f}")
    print(f"Vega:  {vega:.6f}")
    print(f"Theta: {theta:.6f}")
    print(f"Rho:   {rho:.6f}")


if __name__ == "__main__":
    main()
