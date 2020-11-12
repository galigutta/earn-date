from lxml import html
from bs4 import  BeautifulSoup
from time import sleep
from selenium import webdriver
import pandas as pd
import boto3
from selenium.webdriver.chrome.options import Options

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

df = pd.read_csv(fname,header = None)
tl = list(df[0])[:3]
dfEar = pd.DataFrame(columns = ['Ticker','Date'])

driver = webdriver.Chrome(options=set_chrome_options())

for i in tl:
    url = 'https://ycharts.com/companies/'+i+'/events/#/?eventTypes=earnings,&pageNum=1'
    print(url)
    driver.get(url)
    driver.implicitly_wait(10)
    soup = BeautifulSoup(driver.page_source)
    table = soup.find_all('table')[1]
    rows = table.find_all('tr')
    print(i)
    for tr in rows:
        th = tr.find_all('th')
        row = [i.text for i in th]
        ed = row[0].strip()
        dfEar = dfEar.append(pd.DataFrame([[i,ed]],columns = ['Ticker','Date']))
    sleep(10)

dfEar.to_csv('earDateYC.csv', index = False)
driver.close()

with open("earDateYC.csv", "rb") as f:
    s3.upload_fileobj(f, "earn-dt", "edate.csv")