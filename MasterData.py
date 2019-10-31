from imports import *

def GetDividends(tmp):
    dividend_arr = np.zeros(len(tmp))
    for index, symbol in enumerate(tmp['Symbol']):
        lst = []
        year = int(tmp['Date'].iloc[index].year)
        month = int(tmp['Date'].iloc[index].month)
        day = int(tmp['Date'].iloc[index].day)
        lst.append(year)
        lst.append(month)
        lst.append(day)
        dividends = Fetcher(str(symbol), lst).getDividends()
        dividend_arr[index] = np.sum(dividends['Dividends'])*tmp['Quantity'].iloc[index]
    return dividend_arr


df = pd.read_excel('EQUITIES LISTING.xlsx')
df = df.dropna()
df = df.set_index('Account')
df.index = df.index.astype('int64')
df['Date'] = pd.to_datetime(df['Date'])

data = {}
master = {}

for key in df.index:
    value = [df.at[key, 'Symbol'], df.at[key, 'Date'], df.at[key, 'Quantity'],
            df.at[key, 'Cost'], df.at[key, 'Cost Per Share']]
    data[key] = data.get(key, value)

for account in df.index:
    master[account] = pd.DataFrame()

for acct, df in master.items():
    df['Symbol'] = data[acct][0]
    df['Date'] = data[acct][1]
    df['Date'] = pd.to_datetime(df['Date'])
    df['Quantity'] = data[acct][2]
    df['Cost'] = data[acct][3]
    df['Cost Per Share'] = data[acct][4]

for acct, df in master.items():

    recent_close = []

    for index, ticker in enumerate(df['Symbol']):

        try:
            tmp = Fetcher(str(ticker), [2019, 6, 1]).getHistorical()
            recent_close.append(tmp['Close'].iloc[-1])

        except:
            print(ticker)
            print(index)
            pass

    df['Prev_Close'] = recent_close


for acct, df in master.items():
    df['return'] = (df['Prev_Close'] - df['Cost Per Share']) / (df['Cost Per Share'])
    df['No_Div'] = (df['Quantity'] * df['Prev_Close'])
    divs = GetDividends(df)
    df['Divs'] = divs
    df['Current_Value'] = df['No_Div'] + df['Divs']

with open('data.pickle', 'wb') as f:
    pickle.dump(master, f, pickle.HIGHEST_PROTOCOL)
