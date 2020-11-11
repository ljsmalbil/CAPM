import yfinance as yf
import pandas as pd

from CAPM import CapitalAssetPricingModel

"""
    Test File.
    
    Test File.
"""

period = "1y"

# Security
security_name = "^MSFT"

#security_name = "^RUT"

security = yf.Ticker(security_name)
security_data = security.history(period=period)

# Composite NASDAQ
market_name = "^IXIC"
market = yf.Ticker(market_name)
market_data = market.history(period=period)

# Join the two dfs
monthly_prices = pd.concat([security_data['Close'], market_data['Close']], axis = 1)
monthly_prices.columns = [security_name, market_name]

# Convert to percentages
monthly_returns = monthly_prices.pct_change(1)

# Drop in case values are missing
clean_monthly_returns = monthly_returns.dropna(axis=0)  # drop first missing row



model = CapitalAssetPricingModel(clean_monthly_returns[market_name], clean_monthly_returns[security_name], per=period)
#print(model.CAMP())
print(model.beta())

print(model.equity_risk_premium())


print(model.CAMP())

# Return from start to end:
# Return = EndPrice - BeginPrice / BeginPrice
