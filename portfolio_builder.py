from cleandf import clean_df
import numpy as np
import pandas as pd
from scipy.stats import laplace, norm
from yahoo_historical import Fetcher


tickers = ['SPY', 'QQQ', 'XLK', 'MSFT', 'AAPL', 'RPD', 'SNPS', 'XLU', 'D',
        'SRE','XLV', 'JNJ', 'UNH', 'ABT', 'HCP', 'XLF', 'BRK-B', 'BAC', 'GS']

random_porfolios = 100
simulations = 100000 # Number of forecasts to run for each random portfolio

t = int(input("Length of forecast (days): "))

start = [2016,1,1] # Date to start pulling historical data

max_laplace_return = 0
max_gaussian_return = 0

best_weights = None
best_weights2 = None

df = pd.DataFrame()

for ticker in tickers:

    try:

        tmp = Fetcher(ticker, start).getHistorical()
        tmp = clean_df(tmp)
        df[ticker] = tmp['returns'].values

    except:

        print(ticker)

for portfolio in range(random_porfolios):

    print(portfolio)
    weights = np.random.random(len(tickers))
    weights /= np.sum(weights)

    weights2 = weights.copy()

    portfolio_returns = df.dot(weights)

    # Laplace model
    center, scale = laplace.fit(portfolio_returns)

    # Gaussian model
    mu, sigma = norm.fit(portfolio_returns)

    end_returns_laplace = []
    end_returns_gaussian = []

    for simulation in range(simulations):

        laplace_model = np.random.laplace(center, scale, t).cumsum()
        end_returns_laplace.append(laplace_model[-1])

        gaussian_model = np.random.normal(mu, sigma, t).cumsum()
        end_returns_gaussian.append(gaussian_model[-1])

    print([np.average(end_returns_laplace), np.std(end_returns_laplace)])
    print([np.average(end_returns_gaussian), np.std(end_returns_gaussian)])

    if np.average(end_returns_laplace) > max_laplace_return:
        
        max_laplace_return = np.average(end_returns_laplace)
        best_weights = weights

    if  np.average(end_returns_gaussian) > max_gaussian_return:

        max_gaussian_return = np.average(end_returns_gaussian)
        best_weights2 = weights2

print("Max Laplace Return: ", max_laplace_return)
print("Max Gaussian Return: ", max_gaussian_return)

output = pd.DataFrame(columns = ['Tickers', 'Laplace Weights', 'Gaussian Weights'])
output['Tickers'] = tickers
output['Laplace Weights'] = best_weights
output['Gaussian Weights'] = best_weights2
output = output.set_index('Tickers')
output.to_excel("alex_simulation.xlsx")
