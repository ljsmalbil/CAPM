"""

Developed by L. Smalbil

This is the main script and determines the expected return on investment for a given stock.

To be improved later on:

* Error handling
* Inclusion of more exchanges
* Dealing with typos and spelling mistakes
* Automated Security Name to Ticker (e.g. Netflix -> NTLX)

"""

import yfinance as yf
import pandas as pd
import time

from CAPM import CapitalAssetPricingModel

if __name__ == "__main__":
    print('Welcome!')
    time.sleep(3)
    period = "1y"

    # Obtain information about the security
    security_name = str(input("Which security are you interested in? Please enter the ticker symbol. ")) #"MSFT"
    security = yf.Ticker(security_name)
    security_data = security.history(period=period)

    # Obtain index information. Composite NASDAQ
    index = str(input("Where is this security traded? The Nasdaq, Dow Jones or the S&P500? "))

    if index == 'Nasdaq':
        market_name = "^IXIC"
        market = yf.Ticker(market_name)
        market_data = market.history(period=period)
    elif index == 'Dow Jones':
        market_name = "^DJI"
        market = yf.Ticker(market_name)
        market_data = market.history(period=period)
    elif index == '^GSPC':
        market_name = '^GSPC'
        market = yf.Ticker(market_name)
        market_data = market.history(period=period)
    else:
        print('I did not quite catch that. Please try again.')

    # Join the two dfs
    monthly_prices = pd.concat([security_data['Close'], market_data['Close']], axis=1)
    monthly_prices.columns = [security_name, market_name]

    # Convert to percentages
    monthly_returns = monthly_prices.pct_change(1)

    # Drop in case values are missing
    clean_monthly_returns = monthly_returns.dropna(axis=0)

    # Instantiate and return the model
    model = CapitalAssetPricingModel(clean_monthly_returns[market_name], clean_monthly_returns[security_name],
                                     per=period)
    print('The expected return on this security according to the CAPM model is:', round(model.CAMP(), 2))

