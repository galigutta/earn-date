from lxml import html
from time import sleep
from edgar import Company, Documents
import pandas as pd
import boto3
from datetime import date,datetime

s3 = boto3.client('s3')
datestr=date.today().strftime("%Y-%m-%d")

# Get the ticker file from SEC. Assumed to be already downloaded to the working folder
tfile = 'ticker.txt'
cols = ['ticker','id']
dfmap = pd.read_csv(tfile, sep='\\t', engine = 'python', header = None)
dfmap.columns = cols
# Change to upper case and pad with leading zeros
dfmap['ticker'] = dfmap['ticker'].str.upper()
dfmap['id'] = dfmap['id'].astype(str).str.zfill(10)

#read the source list of tickers
dft = pd.read_csv('et.csv',header = None)
dft.columns = ['ticker']

#join with the sec ticker master file to add the 'id' column 
dft = dft.merge(dfmap, on='ticker', how='inner')
dft = dft.drop_duplicates()

dfsftcols = ['ticker','earn_datetime']
dfSECFileTimes = pd.DataFrame(columns = dfsftcols)

for row in  dft.itertuples():
    print(row.ticker + ' ' + row.id)
    company = Company(row.ticker, row.id)
    tree = company.get_all_filings(filing_type = "8-K")
    hrefs = tree.xpath('//*[@id="documentsbutton"]')
    descs = tree.xpath('//div[4]/div[4]//td[3]')

    for i in zip(descs,hrefs):
        if i[0].text_content().strip().find(' 2.02 ') > -1 :
            lnk = 'https://www.sec.gov' + i[1].get('href')
            con = Documents(lnk).content
            if con['Accepted'][:4] == '2014':
                break
            sleep(0.5)
            dfSECFileTimes = dfSECFileTimes.append(pd.DataFrame([[row.ticker, con['Accepted']]], columns = dfsftcols))
            print(" ".join([row.ticker, con['Accepted'],lnk]))
    # break
dfSECFileTimes['AfterClose'] = dfSECFileTimes['earn_datetime'].str[11:13].astype(int) >13
dfSECFileTimes.to_csv('SECFileTimes.csv', index = False)

try:
    with open("SECFileTimes.csv", "rb") as f:
        s3.upload_fileobj(f, "earn-dt", "SECFileTimes.csv",ExtraArgs={'ContentType':'text/html','ACL':'public-read'})
except:
    print('Unable to write to S3, probably not running on AWS')