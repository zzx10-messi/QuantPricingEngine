# QuantPricingEngine

QuantPricingEngine is a modular Python project for European option pricing and risk analysis. It combines financial mathematics with software engineering practice, implementing the Black-Scholes framework in a clean, testable, and extensible structure.

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
- Separate modules for instruments, market data, pricing models, and risk analysis
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
from src.instruments import EuropeanOption
from src.market import MarketData
from src.models import BlackScholes
from src.risk import Greeks

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
├── src/
│   ├── instruments/
│   │   ├── __init__.py
│   │   └── option.py
│   ├── market/
│   │   ├── __init__.py
│   │   └── data.py
│   ├── models/
│   │   ├── __init__.py
│   │   ├── base.py
│   │   └── black_scholes.py
│   └── risk/
│       ├── __init__.py
│       └── greeks.py
├── tests/
│   ├── test_black_scholes.py
│   ├── test_greeks.py
│   ├── test_market.py
│   └── test_option.py
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

## Future Development

Planned extensions include:

- Binomial tree pricing models
- Monte Carlo simulation
- Exotic option pricing
- More advanced volatility and stochastic models

## License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.
