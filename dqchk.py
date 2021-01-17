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

print(dfm.dtypes)

# data fix code goes here

# WFC datafix
# yc data seems to be correct and SEC data has missing history
# 1. backfill data from yc to sec earn date column which is primary, default Afterclose to False
dfm.loc[(dfm['Ticker']=='WFC') & (dfm['AfterClose'].isnull()),'AfterClose'] = False

#DIS datafix
#Missing SEC Data - default to YC AfterClose to True
dfm.loc[(dfm['Ticker']=='DIS') & (dfm['AfterClose'].isnull()),'AfterClose'] = True

#T datafix
# yc data is wrong for 2019-10-23 delete row
dfm = dfm[(dfm['Ticker'] != 'T') | (dfm['Date'] != dt.datetime.strptime('2019/10/23','%Y/%m/%d'))]
# keep earliest
dup = dfm[(dfm['Ticker'] == 'T') & (dfm['Date'] == dt.datetime.strptime('2019/10/28','%Y/%m/%d'))].index.tolist()
dfm = dfm.loc[~dfm.index.isin(dup[0:-1])]
dfm.loc[dup[-1],'yc']='sec'
#set future dates to False for after 2021 and the rest to True
dfm.loc[(dfm['Ticker'] == 'T') & (dfm['Date'].astype('str').str.slice(0, 4).astype('int')>2020) ,'AfterClose'] = False 
dfm.loc[(dfm['Ticker'] == 'T') & (dfm['AfterClose'].isnull()),'AfterClose'] = True 

#PG datafix
#delete 2 wrong dates from yc
dfm = dfm[(dfm['Ticker'] != 'PG') | (dfm['Date'] != dt.datetime.strptime('2020/04/21','%Y/%m/%d'))]
dfm = dfm[(dfm['Ticker'] != 'PG') | (dfm['Date'] != dt.datetime.strptime('2018/04/20','%Y/%m/%d'))]
dfm.loc[(dfm['Ticker']=='PG') & (dfm['AfterClose'].isnull()),'AfterClose'] = False
dfm.loc[(dfm['Ticker']=='PG') & (dfm['yc'].isnull()),'yc']='sec'

# C datafix - Bunch of restatements deleting them
dfm = dfm[(dfm['Ticker'] != 'C') | (dfm['yc'] =='yc')]
dfm.loc[(dfm['Ticker']=='C') & (dfm['AfterClose'].isnull()),'AfterClose'] = False

# JPM - Clean filings - Default to yc
dfm.loc[(dfm['Ticker']=='JPM') & (dfm['AfterClose'].isnull()),'AfterClose'] = False

# AVGO data fix - ticker change - missing rows!
dfm = dfm.append(pd.DataFrame([['AVGO',np.NaN,True,dt.datetime.strptime('2016/6/2','%Y/%m/%d'),'man',np.NaN],
                              ['AVGO',np.NaN,True,dt.datetime.strptime('2016/3/3','%Y/%m/%d'),'man',np.NaN]],
                              columns = dfm.columns
                              ),
                )
dfm.loc[(dfm['Ticker']=='AVGO') & (dfm['AfterClose'].isnull()),'AfterClose'] = True

# PYPL datafix - extra 2.02 filings with SEC
dfm = dfm[(dfm['Ticker'] != 'PYPL') | (dfm['Date'] != dt.datetime.strptime('2016/04/12','%Y/%m/%d'))]
dfm = dfm[(dfm['Ticker'] != 'PYPL') | (dfm['Date'] != dt.datetime.strptime('2019/04/09','%Y/%m/%d'))]
dfm = dfm[(dfm['Ticker'] != 'PYPL') | (dfm['Date'] != dt.datetime.strptime('2019/07/09','%Y/%m/%d'))]
dfm = dfm[(dfm['Ticker'] != 'PYPL') | (dfm['Date'] != dt.datetime.strptime('2019/10/08','%Y/%m/%d'))]
dfm = dfm[(dfm['Ticker'] != 'PYPL') | (dfm['Date'] != dt.datetime.strptime('2020/01/09','%Y/%m/%d'))]
dfm = dfm[(dfm['Ticker'] != 'PYPL') | (dfm['Date'] != dt.datetime.strptime('2020/04/09','%Y/%m/%d'))]
dfm.loc[(dfm['Ticker']=='PYPL') & (dfm['AfterClose'].isnull()),'AfterClose'] = True
dfm.loc[(dfm['Ticker']=='PYPL') & (dfm['yc'].isnull()),'yc']='sec'

# COST datafix - looks like a bunch of late SEC files
dfm = dfm[(dfm['Ticker'] != 'COST') | (dfm['Date'] != dt.datetime.strptime('2017/03/03','%Y/%m/%d'))]
dfm = dfm[(dfm['Ticker'] != 'COST') | (dfm['Date'] != dt.datetime.strptime('2016/05/26','%Y/%m/%d'))]
dfm = dfm[(dfm['Ticker'] != 'COST') | (dfm['Date'] != dt.datetime.strptime('2016/03/03','%Y/%m/%d'))]
dfm = dfm[(dfm['Ticker'] != 'COST') | (dfm['Date'] != dt.datetime.strptime('2015/12/09','%Y/%m/%d'))]
dfm.loc[(dfm['Ticker']=='COST') & (dfm['AfterClose'].isnull()),'AfterClose'] = True

# GS Datafix - couple of unrelated 2.02 filings.
dfm = dfm[(dfm['Ticker'] != 'GS') | (dfm['Date'] != dt.datetime.strptime('2020/10/22','%Y/%m/%d'))]
dfm = dfm[(dfm['Ticker'] != 'GS') | (dfm['Date'] != dt.datetime.strptime('2020/07/24','%Y/%m/%d'))]
dfm.loc[(dfm['Ticker']=='GS') & (dfm['AfterClose'].isnull()),'AfterClose'] = False

#XOM Datafix code - a bunch of unrelated 2.02 filings removing them in one go
dfm = dfm[(dfm['Ticker'] != 'XOM') | ~(dfm['yc'].isnull())]
dfm.loc[(dfm['Ticker']=='XOM') & (dfm['AfterClose'].isnull()),'AfterClose'] = False

#NEE datafix Clean data - just default to yc dates for probably a ticker change
dfm.loc[(dfm['Ticker']=='NEE') & (dfm['AfterClose'].isnull()),'AfterClose'] = False

#INTU datafix - a missing datapoint in YC, rest are unrelated 2.02 filings
dfm.loc[(dfm['Ticker']=='INTU') & (dfm['Date'] == dt.datetime.strptime('2016/02/25','%Y/%m/%d')),'yc']='sec'
dfm = dfm[(dfm['Ticker'] != 'INTU') | ~(dfm['yc'].isnull())]
dfm.loc[(dfm['Ticker']=='INTU') & (dfm['AfterClose'].isnull()),'AfterClose'] = True

#GOOG Datafix - yc has a wrong date for 2020-10-28. delete that and fix rest
dfm = dfm[(dfm['Ticker'] != 'GOOG') | (dfm['Date'] != dt.datetime.strptime('2020/10/28','%Y/%m/%d'))]
dfm.loc[(dfm['Ticker']=='GOOG') & (dfm['yc'].isnull()),'yc']='sec'
dfm.loc[(dfm['Ticker']=='GOOG') & (dfm['AfterClose'].isnull()),'AfterClose'] = True

#BKNG datafix - SEC filings look to be recorded later deleting those
dfm = dfm[(dfm['Ticker'] != 'BKNG') | ~(dfm['yc'].isnull())]
dfm.loc[(dfm['Ticker']=='BKNG') & (dfm['AfterClose'].isnull()),'AfterClose'] = True

#VZ clean data - just missing sec records probably ticker change
dfm.loc[(dfm['Ticker']=='VZ') & (dfm['AfterClose'].isnull()),'AfterClose'] = False

#MDT datafix - looks like a couple of extra random dates
# not fixing the Date 11/24, which is actually 11/23
dfm = dfm[(dfm['Ticker'] != 'MDT') | (dfm['Date'] != dt.datetime.strptime('2017/11/28','%Y/%m/%d'))]
dfm = dfm[(dfm['Ticker'] != 'MDT') | (dfm['Date'] != dt.datetime.strptime('2017/11/08','%Y/%m/%d'))]
dfm = dfm[(dfm['Ticker'] != 'MDT') | (dfm['Date'] != dt.datetime.strptime('2015/05/19','%Y/%m/%d'))]
dfm.loc[(dfm['Ticker']=='MDT') & (dfm['yc'].isnull()),'yc']='sec'
dfm.loc[(dfm['Ticker']=='MDT') & (dfm['AfterClose'].isnull()),'AfterClose'] = False

#CRM Datafix A few extr SEC filings
dfm = dfm[(dfm['Ticker'] != 'CRM') | (dfm['Date'] != dt.datetime.strptime('2018/04/02','%Y/%m/%d'))]
dfm = dfm[(dfm['Ticker'] != 'CRM') | (dfm['Date'] != dt.datetime.strptime('2016/08/29','%Y/%m/%d'))]
dfm = dfm[(dfm['Ticker'] != 'CRM') | (dfm['Date'] != dt.datetime.strptime('2016/02/25','%Y/%m/%d'))]
dfm.loc[(dfm['Ticker']=='CRM') & (dfm['yc'].isnull()),'yc']='sec'
dfm.loc[(dfm['Ticker']=='CRM') & (dfm['AfterClose'].isnull()),'AfterClose'] = True

#PFE datafix extra SEC filings / yc issues
dfm = dfm[(dfm['Ticker'] != 'PFE') | (dfm['Date'] != dt.datetime.strptime('2016/02/16','%Y/%m/%d'))]
dfm = dfm[(dfm['Ticker'] != 'PFE') | (dfm['Date'] != dt.datetime.strptime('2019/07/30','%Y/%m/%d'))]
dfm.loc[(dfm['Ticker']=='PFE') & (dfm['yc'].isnull()),'yc']='sec'
dfm.loc[(dfm['Ticker']=='PFE') & (dfm['AfterClose'].isnull()),'AfterClose'] = False

#UPS datafix
dfm = dfm[(dfm['Ticker'] != 'UPS') | (dfm['Date'] != dt.datetime.strptime('2015/01/23','%Y/%m/%d'))]
dfm = dfm[(dfm['Ticker'] != 'UPS') | (dfm['Date'] != dt.datetime.strptime('2019/07/25','%Y/%m/%d'))]
dfm.loc[(dfm['Ticker']=='UPS') & (dfm['yc'].isnull()),'yc']='sec'
dfm.loc[(dfm['Ticker']=='UPS') & (dfm['AfterClose'].isnull()),'AfterClose'] = False

#FB datafix - missed and incorrect yc dates
dfm = dfm[(dfm['Ticker'] != 'FB') | (dfm['Date'] != dt.datetime.strptime('2020/07/29','%Y/%m/%d'))]
dfm.loc[(dfm['Ticker']=='FB') & (dfm['yc'].isnull()),'yc']='sec'
dfm.loc[(dfm['Ticker']=='FB') & (dfm['AfterClose'].isnull()),'AfterClose'] = True

#ABT Datafix duplicate SEC filings and a bad yc date
dfm = dfm[(dfm['Ticker'] != 'ABT') | (dfm['Date'] != dt.datetime.strptime('2015/01/27','%Y/%m/%d'))]
dfm = dfm[(dfm['Ticker'] != 'ABT') | (dfm['Date'] != dt.datetime.strptime('2017/01/24','%Y/%m/%d'))]
dfm = dfm[(dfm['Ticker'] != 'ABT') | (dfm['Date'] != dt.datetime.strptime('2017/04/17','%Y/%m/%d'))]
dfm = dfm[(dfm['Ticker'] != 'ABT') | (dfm['earn_datetime'] != '2017-01-25 08:00:58')]
dfm.loc[(dfm['Ticker']=='ABT') & (dfm['AfterClose'].isnull()),'AfterClose'] = False

#FISV datafix - additional sec filings
dfm = dfm[(dfm['Ticker'] != 'FISV') | (dfm['Date'] != dt.datetime.strptime('2019/01/16','%Y/%m/%d'))]
dfm = dfm[(dfm['Ticker'] != 'FISV') | (dfm['Date'] != dt.datetime.strptime('2019/10/03','%Y/%m/%d'))]
dfm = dfm[(dfm['Ticker'] != 'FISV') | (dfm['Date'] != dt.datetime.strptime('2020/04/01','%Y/%m/%d'))]
dfm.loc[(dfm['Ticker']=='FISV') & (dfm['AfterClose'].isnull()),'AfterClose'] = True

#CMG datafix - Duplicate Sec Filings, and one missing SEC filing!  
dfm = dfm[(dfm['Ticker'] != 'CMG') | (dfm['earn_datetime'] != '2018-07-26 16:13:51')]
dfm = dfm[(dfm['Ticker'] != 'CMG') | (dfm['Date'] != dt.datetime.strptime('2017/01/10','%Y/%m/%d'))]
dfm = dfm[(dfm['Ticker'] != 'CMG') | (dfm['Date'] != dt.datetime.strptime('2016/01/06','%Y/%m/%d'))]
dfm.loc[(dfm['Ticker']=='CMG') & (dfm['AfterClose'].isnull()),'AfterClose'] = True

#MA datafix 
dfm = dfm[(dfm['Ticker'] != 'MA') | (dfm['Date'] != dt.datetime.strptime('2016/07/14','%Y/%m/%d'))]
dfm = dfm[(dfm['Ticker'] != 'MA') | (dfm['Date'] != dt.datetime.strptime('2018/01/31','%Y/%m/%d'))]
dfm.loc[(dfm['Ticker']=='MA') & (dfm['yc'].isnull()),'yc']='sec'
dfm.loc[(dfm['Ticker']=='MA') & (dfm['AfterClose'].isnull()),'AfterClose'] = False

#TWTR datafix duplicate and missing yc dates
dfm = dfm[(dfm['Ticker'] != 'TWTR') | (dfm['earn_datetime'] != '2019-02-07 11:31:33')]
dfm = dfm[(dfm['Ticker'] != 'TWTR') | (dfm['Date'] != dt.datetime.strptime('2015/10/13','%Y/%m/%d'))]
dfm.loc[(dfm['Ticker']=='TWTR') & (dfm['yc'].isnull()),'yc']='sec'
dfm.loc[(dfm['Ticker']=='TWTR') & (dfm['AfterClose'].isnull()),'AfterClose'] = True

#CMCSA Datafix - missing  SEC filings
dfm = dfm[(dfm['Ticker'] != 'CMCSA') | (dfm['Date'] != dt.datetime.strptime('2019/02/04','%Y/%m/%d'))]
dfm.loc[(dfm['Ticker']=='CMCSA') & (dfm['AfterClose'].isnull()),'AfterClose'] = False

#KO datafix incorrect yc date
dfm = dfm[(dfm['Ticker'] != 'KO') | (dfm['Date'] != dt.datetime.strptime('2018/02/13','%Y/%m/%d'))]
dfm.loc[(dfm['Ticker']=='KO') & (dfm['yc'].isnull()),'yc']='sec'
dfm.loc[(dfm['Ticker']=='KO') & (dfm['AfterClose'].isnull()),'AfterClose'] = False

#INTC datafix missing sec filings
dfm.loc[(dfm['Ticker']=='INTC') & (dfm['AfterClose'].isnull()),'AfterClose'] = True

#MCD datafix extra SEC Filings - probably pre announcements
dfm = dfm[(dfm['Ticker'] != 'MCD') | (dfm['Date'] != dt.datetime.strptime('2020/10/08','%Y/%m/%d'))]
dfm = dfm[(dfm['Ticker'] != 'MCD') | (dfm['Date'] != dt.datetime.strptime('2020/04/08','%Y/%m/%d'))]
dfm.loc[(dfm['Ticker']=='MCD') & (dfm['yc'].isnull()),'yc']='sec'
dfm.loc[(dfm['Ticker']=='MCD') & (dfm['AfterClose'].isnull()),'AfterClose'] = False

#HD datafix - future earnings date not present
dfm = dfm[(dfm['Ticker'] != 'HD') | (dfm['Date'] != dt.datetime.strptime('2016/05/16','%Y/%m/%d'))]
dfm.loc[(dfm['Ticker']=='HD') & (dfm['yc'].isnull()),'yc']='sec'
dfm.loc[(dfm['Ticker']=='HD') & (dfm['AfterClose'].isnull()),'AfterClose'] = False

#AMZN datafix - incorrect yc date
dfm = dfm[(dfm['Ticker'] != 'AMZN') | (dfm['Date'] != dt.datetime.strptime('2015/07/09','%Y/%m/%d'))]
dfm.loc[(dfm['Ticker']=='AMZN') & (dfm['yc'].isnull()),'yc']='sec'
dfm.loc[(dfm['Ticker']=='AMZN') & (dfm['AfterClose'].isnull()),'AfterClose'] = True

#BAC datafix duplicate yc entry
dfm = dfm[(dfm['Ticker'] != 'BAC') | (dfm['Date'] != dt.datetime.strptime('2015/02/26','%Y/%m/%d'))]
dfm.loc[(dfm['Ticker']=='BAC') & (dfm['yc'].isnull()),'yc']='sec'
dfm.loc[(dfm['Ticker']=='BAC') & (dfm['AfterClose'].isnull()),'AfterClose'] = False

#MSFT datafix duplicate yc entry
dfm = dfm[(dfm['Ticker'] != 'MSFT') | (dfm['Date'] != dt.datetime.strptime('2018/04/27','%Y/%m/%d'))]
dfm.loc[(dfm['Ticker']=='MSFT') & (dfm['yc'].isnull()),'yc']='sec'
dfm.loc[(dfm['Ticker']=='MSFT') & (dfm['AfterClose'].isnull()),'AfterClose'] = True

#PEP datafix accepted on an earlier date than filing date!
dfm = dfm[(dfm['Ticker'] != 'PEP') | (dfm['Date'] != dt.datetime.strptime('2020/09/30','%Y/%m/%d'))]
dfm.loc[(dfm['Ticker']=='PEP') & (dfm['AfterClose'].isnull()),'AfterClose'] = False

#ADBE Datafix - couple of missing yc dates
dfm.loc[(dfm['Ticker']=='ADBE') & (dfm['yc'].isnull()),'yc']='sec'
dfm.loc[(dfm['Ticker']=='ADBE') & (dfm['AfterClose'].isnull()),'AfterClose'] = True

#TMO datafix - couple of extra sec filings in 2020
dfm = dfm[(dfm['Ticker'] != 'TMO') | (dfm['Date'] != dt.datetime.strptime('2020/07/06','%Y/%m/%d'))]
dfm = dfm[(dfm['Ticker'] != 'TMO') | (dfm['Date'] != dt.datetime.strptime('2020/04/06','%Y/%m/%d'))]
dfm.loc[(dfm['Ticker']=='TMO') & (dfm['AfterClose'].isnull()),'AfterClose'] = False

#SNAP datafix 
dfm = dfm[(dfm['Ticker'] != 'SNAP') | (dfm['Date'] != dt.datetime.strptime('2019-01-15','%Y-%m-%d'))]
dfm.loc[(dfm['Ticker']=='SNAP') & (dfm['yc'].isnull()),'yc']='sec'
dfm.loc[(dfm['Ticker']=='SNAP') & (dfm['AfterClose'].isnull()),'AfterClose'] = True

#AMD datafix - additional SEC filings
dfm = dfm[(dfm['Ticker'] != 'AMD') | (dfm['Date'] != dt.datetime.strptime('2018-02-27','%Y-%m-%d'))]
dfm = dfm[(dfm['Ticker'] != 'AMD') | (dfm['Date'] != dt.datetime.strptime('2015-07-06','%Y-%m-%d'))]
dfm.loc[(dfm['Ticker']=='AMD') & (dfm['AfterClose'].isnull()),'AfterClose'] = True

#QCOM datafix
dfm = dfm[(dfm['Ticker'] != 'QCOM') | (dfm['Date'] != dt.datetime.strptime('2020-01-30','%Y-%m-%d'))]
dfm.loc[(dfm['Ticker']=='QCOM') & (dfm['yc'].isnull()),'yc']='sec'
dfm.loc[(dfm['Ticker']=='QCOM') & (dfm['AfterClose'].isnull()),'AfterClose'] = True

#DPZ datafix - duplicate SEC filings
dfm = dfm[(dfm['Ticker'] != 'DPZ') | (dfm['earn_datetime'] != '2015-02-24 07:31:29')]
dfm = dfm[(dfm['Ticker'] != 'DPZ') | (dfm['Date'] != dt.datetime.strptime('2015-09-28','%Y-%m-%d'))]
dfm = dfm[(dfm['Ticker'] != 'DPZ') | (dfm['Date'] != dt.datetime.strptime('2020-03-30','%Y-%m-%d'))]
dfm.loc[(dfm['Ticker']=='DPZ') & (dfm['AfterClose'].isnull()),'AfterClose'] = False


#NFLX datafix - couple of extra sec filings
dfm = dfm[(dfm['Ticker'] != 'NFLX') | (dfm['Date'] != dt.datetime.strptime('2019-12-16','%Y-%m-%d'))]
dfm = dfm[(dfm['Ticker'] != 'NFLX') | (dfm['Date'] != dt.datetime.strptime('2019-01-02','%Y-%m-%d'))]
dfm.loc[(dfm['Ticker']=='NFLX') & (dfm['AfterClose'].isnull()),'AfterClose'] = True

#UNH datafix - missing yc date
dfm.loc[(dfm['Ticker']=='UNH') & (dfm['yc'].isnull()),'yc']='sec'
dfm.loc[(dfm['Ticker']=='UNH') & (dfm['AfterClose'].isnull()),'AfterClose'] = False

#TXN datafix
dfm = dfm[(dfm['Ticker'] != 'TXN') | (dfm['Date'] != dt.datetime.strptime('2018-07-18','%Y-%m-%d'))]
dfm.loc[(dfm['Ticker']=='TXN') & (dfm['AfterClose'].isnull()),'AfterClose'] = True

#ORCL datafix
dfm.loc[(dfm['Ticker']=='ORCL') & (dfm['yc'].isnull()),'yc']='sec'
dfm.loc[(dfm['Ticker']=='ORCL') & (dfm['AfterClose'].isnull()),'AfterClose'] = True

#NVDA datafix
dfm = dfm[(dfm['Ticker'] != 'NVDA') | (dfm['Date'] != dt.datetime.strptime('2019-01-28','%Y-%m-%d'))]
dfm.loc[(dfm['Ticker']=='NVDA') & (dfm['AfterClose'].isnull()),'AfterClose'] = True

#JNJ datafix
dfm = dfm[(dfm['Ticker'] != 'JNJ') | (dfm['Date'] != dt.datetime.strptime('2019-10-23','%Y-%m-%d'))]
dfm.loc[(dfm['Ticker']=='JNJ') & (dfm['AfterClose'].isnull()),'AfterClose'] = False

#BMY datafix missing sec - too back dated to be pulled in script
dfm.loc[(dfm['Ticker']=='BMY') & (dfm['AfterClose'].isnull()),'AfterClose'] = False

#AAPL datafix - one preannouncement
dfm = dfm[(dfm['Ticker'] != 'AAPL') | (dfm['Date'] != dt.datetime.strptime('2019-01-02','%Y-%m-%d'))]
dfm.loc[(dfm['Ticker']=='AAPL') & (dfm['AfterClose'].isnull()),'AfterClose'] = True

#CVX datafix
dfm = dfm[(dfm['Ticker'] != 'CVX') | (dfm['earn_datetime'] != '2016-01-29 15:43:08')]
dfm.loc[(dfm['Ticker']=='CVX') & (dfm['AfterClose'].isnull()),'AfterClose'] = False

#ZM and others
dfm.loc[(dfm['Ticker']=='ZM') & (dfm['AfterClose'].isnull()),'AfterClose'] = True
dfm.loc[(dfm['Ticker']=='V') & (dfm['AfterClose'].isnull()),'AfterClose'] = True
dfm.loc[(dfm['Ticker']=='TTD') & (dfm['AfterClose'].isnull()),'AfterClose'] = True
dfm.loc[(dfm['Ticker']=='MRK') & (dfm['AfterClose'].isnull()),'AfterClose'] = False
dfm.loc[(dfm['Ticker']=='CSCO') & (dfm['AfterClose'].isnull()),'AfterClose'] = True
dfm.loc[(dfm['Ticker']=='CME') & (dfm['AfterClose'].isnull()),'AfterClose'] = False
dfm.loc[(dfm['Ticker']=='ATVI') & (dfm['AfterClose'].isnull()),'AfterClose'] = True
dfm.loc[(dfm['Ticker']=='ADP') & (dfm['AfterClose'].isnull()),'AfterClose'] = False

# End of datafix code 

dfmnan = dfm[dfm['yc'].isnull() | dfm['AfterClose'].isnull()  ]
dfq = dfmnan.groupby(['Ticker'])['Ticker'].count().sort_values(ascending = False)

ticker = 'ADP'
dfmnanticker = dfmnan[dfmnan['Ticker']==ticker]
dfmallticker = dfm[dfm['Ticker']==ticker].sort_values('Date', ascending = False)

print (dfmallticker.shape)
print(dfmallticker)
print(dfq.head())


