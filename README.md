# QuantPricingEngine

QuantPricingEngine is a pricing-focused Python library for option products. The
current milestone implements European options, Black-Scholes analytical pricing,
Greeks, and robust implied-volatility inversion. Tree, Monte Carlo, and finite
difference engines are planned as later pricing milestones.

## Project Overview

This project demonstrates a practical application of quantitative finance concepts in Python. The current implementation focuses on:

- Modeling European call and put options
- Pricing options using the Black-Scholes analytical model
- Calculating the main option Greeks: Delta, Gamma, Vega, Theta, and Rho
- Building a modular codebase suitable for future expansion into more advanced pricing methods

## Why This Project Matters

For a student applying to a Financial Engineering or Quantitative Finance graduate program, this project showcases three important capabilities:

1. **Mathematical Finance Foundation**
   - Strong understanding of derivative pricing theory and risk sensitivities

2. **Programming and Engineering Skills**
   - Clean object-oriented structure, modular package design, and test-driven development

3. **Research and Extension Potential**
   - The codebase is designed to support future work in numerical methods, stochastic models, and more complex derivatives

## Core Features

- European option representation with validation
- Black-Scholes pricing for call and put options
- Analytical Greeks calculation for risk management
- Separate modules for products, analytical pricing, analytics, numerical methods,
  and shared types
- Implied volatility using Brent, bisection, or safeguarded Newton methods
- Automated tests for pricing and Greeks accuracy

## Mathematical Foundation

The project implements the classical Black-Scholes model for European options.

For a European call option:

$$C = S_0N(d_1) - Ke^{-rT}N(d_2)$$

For a European put option:

$$P = Ke^{-rT}N(-d_2) - S_0N(-d_1)$$

where:

$$d_1 = \frac{\ln(S_0/K) + (r + \frac{1}{2}\sigma^2)T}{\sigma\sqrt{T}}$$

$$d_2 = d_1 - \sigma\sqrt{T}$$

The project also computes the main Greeks, which measure the sensitivity of option value to changes in underlying price, volatility, time, and interest rates.

## Installation

```bash
git clone https://github.com/<your-username>/QuantPricingEngine.git
cd QuantPricingEngine

# Optional: create a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Or install the package in editable mode (recommended for development)
pip install -e ".[dev]"
```

## Quick Start

```python
from option_pricing.analytical import BlackScholes
from option_pricing.analytics import Greeks, ImpliedVolatility
from option_pricing.common import MarketData
from option_pricing.products import EuropeanOption

option = EuropeanOption(
    strike=100,
    maturity=1,
    option_type="call",
)

market = MarketData(
    spot=100,
    rate=0.05,
    volatility=0.2,
)

model = BlackScholes()
price = model.price(option, market)

greeks = Greeks(model)

print(f"Price: {price:.6f}")
print(f"Delta: {greeks.delta(option, market):.6f}")

implied_vol = ImpliedVolatility(model).solve(option, market, price)
print(f"Implied volatility: {implied_vol:.6f}")
```

You can also run the bundled example:

```bash
python main.py
```

Example output:

```text
Price: 10.450584
Delta: 0.636831
```

## Project Structure

```text
QuantPricingEngine/
├── option_pricing/
│   ├── products/
│   │   └── european.py
│   ├── analytical/
│   │   └── black_scholes.py
│   ├── analytics/
│   │   ├── greeks.py
│   │   └── implied_volatility.py
│   ├── numerical/
│   │   └── root_finding.py
│   └── common/
│       ├── enums.py
│       ├── exceptions.py
│       ├── market.py
│       ├── result.py
│       └── validation.py
├── tests/
│   ├── test_black_scholes.py
│   ├── test_greeks.py
│   ├── test_market.py
│   ├── test_option.py
│   └── test_implied_volatility.py
├── main.py
├── pyproject.toml
├── pytest.ini
├── requirements.txt
├── LICENSE
└── README.md
```

## Testing

The project uses pytest for automated validation.

```bash
pytest
```

Current tests cover:

- Option validation (strike, maturity, type)
- Market data validation (spot, rate, volatility)
- Black-Scholes pricing accuracy for calls and puts
- Put-call parity
- Greek calculation correctness for calls and puts
- Implied-volatility convergence, no-arbitrage bounds, bracket expansion, and
  difficult Newton cases

## Future Development

Planned extensions include:

- Binomial tree pricing models
- Monte Carlo simulation
- Exotic option pricing
- Finite-difference pricing

The project deliberately focuses on pricing engines. Volatility-surface
construction is outside the current scope.

## License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.
