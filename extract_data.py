# import necessary packages
import pandas as pd
from pycoingecko import CoinGeckoAPI
import numpy as np

# create a client
cg = CoinGeckoAPI()

# confirm connection
cg.ping()

# get a list of coins, sort df by id
coinList = cg.get_coins_list()
coinDataFrame = pd.DataFrame.from_dict(coinList).sort_values('id').reset_index(drop=True)

# Call crypto btc/eth/dpx by API id
# coinDataFrame[coinDataFrame['id'] == 'bitcoin']
# coinDataFrame[coinDataFrame['id'] == 'ethereum']

# import cryptos from Index CIX100
cix100 = pd.read_csv('data/cix100_coins.csv')

# import all cryptos from CoinGecko API
coinsgecko = coinDataFrame.merge(cix100, how='inner', on='name')

# get data
coins_merge = coinsgecko.merge(cix100, how='right', on='name')
coins = coins_merge['id']
# compiled for eliminating missing values
# coins_filter = cix100[(~cix100.name.isin(coinsgecko.name))]
# print(coins_merge)

# convert to a list
coins_list = list(coins_merge['id'])

# print(sorted(coins_list))

# get list of suppored VS currencies
counterCurrencies = cg.get_supported_vs_currencies()
vsCurrencies = ['usd', 'eur']

# simple price request - nested dictionary format

simplePriceRequest = cg.get_price(ids=coins_list, vs_currencies='eur')

# simple data validation
# print(len(simplePriceRequest))
# check_list = []
# for k, v in simplePriceRequest.items():
#     for k1,v1 in v.items():
#         check_list.append(k)

# price request
# PriceRequest = cg.get_price(ids = coins_list,
#                             vs_currencies = vsCurrencies,
#                             include_market_cap = False,
#                             include_24hr_vol = False,
#                             include_24hr_change = True,
#                             include_last_updated_at = False,
#                             precision = 4)

# complex data validation
# print(len(PriceRequest))
# check_coins = []
# for p, n in PriceRequest.items():
#     for p1,n1 in n.items():
#         check_coins.append(p)
# print(len(set(check_coins)))


# #get daily historical data for all crypto
# for idx, x in enumerate(coins):
#      getDailyHistoricalDatabyID(x,cg)
#      print('\n', x, ' ', idx+1)

# get daily historical data per crypto-ID
# bitcoin = getHistoricalDatabyID('bitcoin',cg)
# ethereum = getHistoricalDatabyID('ethereum',cg)

# print('ethereum','\n', getDailyHistoricalDatabyID('ethereum',cg))
