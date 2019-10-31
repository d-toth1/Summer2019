from cleandf import clean_df
import matplotlib.pyplot as plt
import numpy as np
from distributions import Laplace
import pandas as pd
from yahoo_historical import Fetcher
from scipy.stats import norm
import sys

def sim_returns(ticker, start, dist="Laplace", end=None, t=365, trials=100000):

    """
    Function to simulate the future returns of a
    particular stock.

    Pulls historical stock data from Yahoo Finance and stores data
    in a pandas dataframe. Computes the daily returns, and fits the return data
    to a Laplace distribution:

    f(x) = 1/(2b) exp( - (abs(x - mu) / b)), where mu (-infinity, infinity), b > 0

    The mu parameter estimated by the sample median, and b (the scale parameter) is estimated
    by the mean deviation from the median.

    Using these parameters, random samples are generated from the distribution and used
    to create Monte Carlo simulations.

    args:

        ticker (str) : symbol of ticker
        start (list) : [yyyy, mm, dd], date at which historical data starts
        dist (str)   : distribution to use (Laplace [default] or Normal)
        end (list)   : [yyyy, mm, dd] date at which historical data ends
        t (int)      : length of interval to simulate -- default = 365
        trials (int) : number of simulations to run -- default = 100,000

    returns:

        (array) Last values of simulated returns
        (float) Average of the last values of the returns across all
                simulations.
        (float) Sample standard deviation of end value of the returns
                across all simulations.
    """

    df = Fetcher(ticker, start, end).getHistorical()
    df = clean_df(df)

    end_returns = []

    if dist == "Laplace":

        center, scale = Laplace.fit(df['returns'])

        for simulation in range(trials):

            sim_returns = np.random.laplace(center, scale, t).cumsum()
            end_returns.append(sim_returns[-1])

        return np.array(end_returns), np.average(end_returns), np.std(end_returns, ddof=1)

    if dist == "Normal":

        center, scale = norm.fit(df['returns'])

        for simulation in range(trials):

            sim_returns = np.random.normal(center, scale, t).cumsum()
            end_returns.append(sim_returns[-1])

        return np.array(end_returns), np.average(end_returns), np.std(end_returns, ddof=1)

ticker = sys.argv[1]
start = [2017,1,1]
print(sim_returns(ticker, start))
