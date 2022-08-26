# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import pandas as pd
import os
import yfinance as yf

def relative_strength_idx(data, n=14):
    close = data['Close']
    delta = close.diff()
    delta = delta[1:]
    pricesUp = delta.copy()
    pricesDown = delta.copy()
    pricesUp[pricesUp < 0] = 0
    pricesDown[pricesDown > 0] = 0
    rollUp = pricesUp.rolling(n).mean()
    rollDown = pricesDown.abs().rolling(n).mean()
    rs = rollUp / rollDown
    rsi = 100.0 - (100.0 / (1.0 + rs))
    return rsi


def get_finance(item):
    #getting the initial data
    data = yf.download(item, start="2022-01-01", end="2022-06-30")
    data.reset_index(inplace=True)
    
    #Moving Averages
    #EMA 9: Exponential Moving Average for the period of 9 days
    data['EMA_9'] = data['Close'].ewm(9).mean().shift()
    #SMA 5: Simple Moving Average for the period of 5 days
    data['SMA_5'] = data['Close'].rolling(5).mean().shift()
    #SMA 10: Simple Moving Average for the period of 10 days
    data['SMA_10'] = data['Close'].rolling(10).mean().shift()
    #SMA 15: Simple Moving Average for the period of 15 days
    data['SMA_15'] = data['Close'].rolling(15).mean().shift()
    #SMA 30: Simple Moving Average for the period of 30 days
    data['SMA_30'] = data['Close'].rolling(30).mean().shift()
    
    #Relative Strength Index
    data['RSI'] = relative_strength_idx(data).fillna(0)
    
    #Moving average convergence divergence 
    EMA_12 = pd.Series(data['Close'].ewm(span=12, min_periods=12).mean())
    EMA_26 = pd.Series(data['Close'].ewm(span=26, min_periods=26).mean())
    data['MACD'] = pd.Series(EMA_12 - EMA_26)
    data['MACD_signal'] = pd.Series(data.MACD.ewm(span=9, min_periods=9).mean())
    
    #Writting the code 
    data.to_csv(os.path.join("Financial_data/{}.csv".format(item)))

df_comp = pd.read_csv('constituents_modified.csv') 
df_comp['Symbol'].apply(get_finance)