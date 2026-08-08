QuantPricingEngine
A Python-based derivatives pricing library for European options.
QuantPricingEngine is a modular Python framework designed for derivatives pricing and risk analysis.

The current version implements the Black-Scholes analytical pricing model and calculates option Greeks for European options.

This project combines financial mathematics with software engineering principles and provides a foundation for future extensions such as numerical pricing methods and advanced volatility models.

Features
Current Features
European option representation
Black-Scholes analytical pricing model
Option Greeks calculation
Supported Greeks
Delta
Gamma
Vega
Theta
Rho
Future Development
Binomial Tree pricing model
Monte Carlo simulation
Exotic option pricing
Stochastic volatility models
Mathematical Background
Black-Scholes Model
For a European call option:
C=S 
0
​	
 N(d 
1
​	
 )−Ke 
−rT
 N(d 
2
​	
 )
where:
d 
1
​	
 = 
σ 
T
​	
 
ln(S 
0
​	
 /K)+(r+ 
2
1
​	
 σ 
2
 )T
​	
 
d 
2
​	
 =d 
1
​	
 −σ 
T
​	
 
For a European put option:
P=Ke 
−rT
 N(−d 
2
​	
 )−S 
0
​	
 N(−d 
1
​	
 )
Model Parameters
Symbol	Description
S0	Current underlying asset price
K	Strike price
T	Time to maturity
r	Risk-free interest rate
σ	Volatility
Greeks
The library calculates the main option risk sensitivities.
Delta
Δ= 
∂S
∂V
​	
 
Sensitivity to changes in the underlying asset price.
Gamma
Γ= 
∂S 
2
 
∂ 
2
 V
​	
 
Measures the rate of change of Delta.
Vega
Vega= 
∂σ
∂V
​	
 
Sensitivity to volatility changes.
Theta
Θ= 
∂t
∂V
​	
 
Measures option time decay.
Rho
ρ= 
∂r
∂V
​	
 
Sensitivity to interest rate changes.
Project Structure
QuantPricingEngine/

├── src/
│
│   ├── instruments/
│   │   ├── __init__.py
│   │   └── option.py
│   │
│   ├── market/
│   │   ├── __init__.py
│   │   └── data.py
│   │
│   ├── models/
│   │   ├── __init__.py
│   │   ├── base.py
│   │   └── black_scholes.py
│   │
│   └── risk/
│       ├── __init__.py
│       └── greeks.py
│
├── tests/
│
├── main.py
├── requirements.txt
├── .gitignore
└── README.md
Installation
Clone the repository:
git clone <repository-url>
Install dependencies:
pip install -r requirements.txt
Usage
Example:
from src.instruments import EuropeanOption
from src.market import MarketData
from src.models import BlackScholes


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


print(price)
Output:
10.450584
Testing
This project uses pytest for automated testing.
Run:

pytest
Tests verify:
Option object validation
Black-Scholes pricing accuracy
Greeks calculation correctness
Design Architecture
The project follows a modular pricing architecture:
Financial Instrument

        +

Market Data

        ↓

Pricing Model

        ↓

Risk Analysis
The pricing model layer is designed for future extensions:
              PricingModel

                    |

        ----------------------------

        |             |            |

Black-Scholes   Binomial Tree   Monte Carlo
Future Roadmap
Version 0.2
Implement Binomial Tree model
Compare numerical and analytical pricing
Version 0.3
Implement Monte Carlo simulation
Add confidence interval estimation
Version 1.0
Support additional derivatives
Add advanced volatility models
License
MIT License


