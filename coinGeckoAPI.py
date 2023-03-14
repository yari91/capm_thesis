# get OHLC data for preset range 1/7/14/30/90/180/365/max
# candle body width by date range
# 1 - 2 days: 30 minutes
# 3 - 30 days: 4 hours
# 31 days and beyond: 4 days
import pandas as pd
import datetime as dt


def getHistoricalDatabyID(crypto_id, cg):
    ohlcData = cg.get_coin_ohlc_by_id(id=crypto_id,
                                      vs_currency='eur',
                                      days='max')
    # list to dataframe
    ohlcDataFrame = pd.DataFrame(data=ohlcData,
                                 columns=['Date', 'Open', 'High', 'Low', 'Close'])
    # reformat date
    ohlcDataFrame['Date'] = ohlcDataFrame['Date'].apply(
        lambda x: dt.datetime.fromtimestamp(x / 1000
                                            ).strftime('%m-%d-%Y %H:%M:%S'))
    # set index
    ohlcDataFrame = ohlcDataFrame.set_index('Date')
    # ohlcDataFrame.to_csv('raw_data.csv', index=True)
    return ohlcDataFrame


def getDailyHistoricalDatabyID(crypto_id, cg):
    dailyHistoricalData = cg.get_coin_market_chart_by_id(id=crypto_id,
                                                         vs_currency='eur',
                                                         days='max')
    # list to dataframe
    dailyDataFrame = pd.DataFrame(data=dailyHistoricalData['prices'],
                                  columns=['Date', 'Price'])

    # reformat date
    dailyDataFrame['Date'] = dailyDataFrame['Date'].apply(
        lambda x: dt.datetime.fromtimestamp(x / 1000
                                            ).strftime('%m-%d-%Y'))

    dailyDataFrame = dailyDataFrame.set_index('Date')
    dailyDataFrame.to_csv('daily/daily_' + crypto_id + '.csv', index=True)
    return dailyDataFrame
