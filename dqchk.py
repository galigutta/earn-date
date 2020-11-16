# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

# importing pandas as pd 
import pandas as pd 

df = pd.read_csv('SECFileTimes.csv')
df.columns=['Ticker']+ list(df.columns[1:])

#df = df[df['Ticker']!='TSLA' ]

dfyc = pd.read_csv('edate.csv',parse_dates = [1])
dfyc['yc']='yc'

dfyc = dfyc[dfyc['Ticker']!='GOOGL' ]
dfyc = dfyc[dfyc['Ticker']!='BABA' ]
#dfyc = dfyc[dfyc['Ticker']!='TSLA' ]

dfyc = dfyc[dfyc['Date'].astype('str').str.slice(0, 4)!='2021']

dfyc = dfyc[dfyc['Date'].astype('str').str.slice(0, 4).astype('int')>2014]


df['Date'] = pd.to_datetime( df['earn_datetime'].str.slice(0, 10)).dt.date
df['Date'] = df['Date'].astype('datetime64[ns]')
dfyc['Date'] = pd.to_datetime(dfyc['Date'],utc = True).astype('datetime64[ns]')

dfm = df.merge(dfyc, on =['Ticker','Date'], how = 'outer')


print(df.dtypes)
print(dfyc.dtypes)

dfmnan = dfm[dfm['yc'].isnull() | dfm['AfterClose'].isnull()  ]

dfq = dfmnan.groupby(['Ticker'])['Ticker'].count().sort_values()

dfmnanticker = dfmnan[dfmnan['Ticker']=='DHR']