import pandas as pd
from yahoo_historical import Fetcher

def clean_df(df):

    df = df.set_index('Date')
    df.index = pd.to_datetime(df.index)
    df['returns'] = df['Close'].pct_change()
    df = df.dropna()

    return df
