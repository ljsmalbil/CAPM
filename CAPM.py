"""

Developed by L. Smalbil

This is an object that builds the CAPM and computes the expected return for a given security

"""

import pandas as pd
import numpy as np
import yfinance as yf

from sklearn import linear_model

class CapitalAssetPricingModel:
    def __init__(self, market, security, market_name = "^IXIC", per="1y"):
        self.security = np.array(security).reshape(-1, 1)
        self.market = np.array(market).reshape(-1, 1)
        self.market_name = market_name
        self.per = per

    def beta(self):
        """
        The beta is defined as follows:

        \beta = covariance(return_on_stock, return_market_overall) / variance(return_market_overall)

        A beta coefficient can measure the volatility of an individual stock compared to the systematic
        risk of the entire market.

        For comparison:

        * . beta = 0 indicates no correlation with the chosen benchmark (e.g. NASDAQ index )
        * . beta = 1 indicates a stock has the same volatility as the market
        * . beta > 1 indicates a stock that’s more volatile than its benchmark
        * . beta < 1 is less volatile than the benchmark

        Thus, a beta of 1.7 is 70% more volatile than the benchmark

        :return:
        """

        reg = linear_model.LinearRegression()
        reg.fit(np.array(self.security), np.array(self.market))

        return 'The beta is:', float(reg.coef_)

    def risk_free_rate(self):
        """
        One of the terms in the CAPM model is the risk-free rate.

        Here the latest 13-week US treasury bill interest rate is used as a proxy
        :return:
        """

        risk_free_rate = yf.Ticker("^IRX")
        risk_free_rate = risk_free_rate.history(period="today")
        return float(risk_free_rate['Open'])

    def equity_risk_premium(self):
        """
        The equity risk premium (erp) is defined as the expected return of a given security minus
        the risk free rate.

        :return:
        """
        market = yf.Ticker(self.market_name)
        market_data = market.history(period=self.per)
        expected_return = (market_data['Close'][-1] - market_data['Close'][0]) / market_data['Close'][0]

        risk_free_rate = yf.Ticker("^IRX")
        risk_free_rate = risk_free_rate.history(period="today")
        erp = expected_return - float(risk_free_rate['Open'])
        return erp, expected_return

    def CAMP(self):
        """
        The CAPM model can be defined as follows:

        Exp_Return_Invest = RiskFreeRate + Beta * (ExpReturnMarket - RiskFreeRate)

        :return:
        """

        # Terms
        risk_free_rate = yf.Ticker("^IRX")
        risk_free_rate = risk_free_rate.history(period="today")
        rfr = float(risk_free_rate['Open'])

        market = yf.Ticker(self.market_name)
        market_data = market.history(period=self.per)
        expected_return_market = (market_data['Close'][-1] - market_data['Close'][0]) / market_data['Close'][0]
        erp = expected_return_market - rfr

        reg = linear_model.LinearRegression()
        reg.fit(np.array(self.security), np.array(self.market))
        beta = float(reg.coef_)

        eri = rfr + (beta * (expected_return_market - rfr))
        return eri
