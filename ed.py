from lxml import html
from bs4 import  BeautifulSoup
from time import sleep
from selenium import webdriver
import pandas as pd
import boto3
from selenium.webdriver.chrome.options import Options
from datetime import date,datetime

def set_chrome_options() -> None:
    """Sets chrome options for Selenium.
    Chrome options for headless browser is enabled.
    """
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_prefs = {}
    chrome_options.experimental_options["prefs"] = chrome_prefs
    chrome_prefs["profile.default_content_settings"] = {"images": 2}
    return chrome_options

fname = 'et.csv'
s3 = boto3.client('s3')
datestr=date.today().strftime("%Y-%m-%d")

df = pd.read_csv(fname,header = None)
tl = list(df[0])
dfEar = pd.DataFrame(columns = ['Ticker','Date'])

driver = webdriver.Chrome(options=set_chrome_options())

for i in tl:
    url = 'https://ycharts.com/companies/'+i+'/events/#/?eventTypes=earnings,&pageNum=1'
    print(url)
    driver.get(url)
    driver.implicitly_wait(10)
    soup = BeautifulSoup(driver.page_source, features="lxml")
    table = soup.find_all('table')[1]
    rows = table.find_all('tr')
    # print(i)
    for tr in rows:
        th = tr.find_all('th')
        row = [i.text for i in th]
        ed = row[0].strip()
        if ed[:1].isnumeric():
            dfEar = dfEar.append(pd.DataFrame([[i,ed]],columns = ['Ticker','Date']))
    sleep(10)

dfEar.to_csv('earDateYC.csv', index = False)
driver.close()

# try:
with open("earDateYC.csv", "rb") as f:
    s3.upload_fileobj(f, "earn-dt", "edate.csv",ExtraArgs={'ContentType':'text/html','ACL':'public-read'})
# need to re-open and archive
with open("earDateYC.csv", "rb") as f:    
    s3.upload_fileobj(f, "earn-dt", "edate_"+datestr+".csv",ExtraArgs={'ContentType':'text/html','ACL':'public-read'})
# except:
#     print('Unable to write to S3, probably not running on AWS')


'''
SEC Code
---
from lxml import html
from edgar import Company, Documents
company = Company('placeholder', "0001633917")
tree = company.get_all_filings(filing_type = "8-K")
hrefs = tree.xpath('//*[@id="documentsbutton"]')
print(len(hrefs))
for i in hrefs[:15]:
    lnk = 'https://www.sec.gov' + i.get('href')
    con = Documents(lnk).content
    if con['Items'][:10] == 'Item 2.02:':
        #print(con['Accepted'])
        print(" ".join([con['Accepted'],lnk]))

join code
import pandas as pd
tfile = 'ticker.txt'
cols = ['ticker','id']
dfmap = pd.read_csv(tfile, sep='\\t', engine = 'python', header = None)
dfmap.columns = cols
dfmap['ticker'] = dfmap['ticker'].str.upper()
dfmap['id'] = dfmap['id'].astype(str).str.zfill(10)

dft = pd.read_csv('et.csv',header = None)
dft.columns = ['ticker']

dft = dft.merge(dfmap, on='ticker', how='inner')
dft = dft.drop_duplicates()

'''