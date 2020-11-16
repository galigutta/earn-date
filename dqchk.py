# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

# importing pandas as pd 
import pandas as pd 
import numpy as np
import datetime as dt

df = pd.read_csv('SECFileTimes.csv')
df.columns=['Ticker']+ list(df.columns[1:])
#filtering problem tickers
df = df[(df['Ticker']!='TSLA') & (df['Ticker']!='DHR')]
#df = df[df['Ticker']!='DHR']

dfyc = pd.read_csv('edate.csv',parse_dates = [1])
dfyc['yc']='yc'
yc_procdate = dt.datetime.strptime('2020/11/12','%Y/%m/%d')

#filtering problem tickers
dfyc = dfyc[(dfyc['Ticker']!='GOOGL') & (dfyc['Ticker']!='BABA')&(dfyc['Ticker']!='TSLA')&(dfyc['Ticker']!='DHR')]

#dfyc = dfyc[dfyc['Date'].astype('str').str.slice(0, 4)!='2021']

#Retain earnings from 2015 and later only
dfyc = dfyc[dfyc['Date'].astype('str').str.slice(0, 4).astype('int')>2014]

# convert both to a datetime format and drop time to join
df['Date'] = pd.to_datetime( df['earn_datetime'].str.slice(0, 10),utc = True).astype('datetime64[ns]')
dfyc['Date'] = pd.to_datetime(dfyc['Date'].astype('str').str.slice(0, 10),utc = True).astype('datetime64[ns]')

dfm = df.merge(dfyc, on =['Ticker','Date'], how = 'outer')
dfm['effEarnDate'] = np.NaN
#Retain all future dates from yc


#print(df.dtypes)
print(dfyc.dtypes)

dfmnan = dfm[dfm['yc'].isnull() | dfm['AfterClose'].isnull()  ]

dfq = dfmnan.groupby(['Ticker'])['Ticker'].count().sort_values(ascending = False)



ticker = 'WFC'
dfmnanticker = dfmnan[dfmnan['Ticker']==ticker]
dfmallticker = dfm[dfm['Ticker']==ticker].sort_values('Date', ascending = False)


print (dfmallticker.shape)
print(dfmallticker)
print(dfq.head())