from lxml import html
from bs4 import  BeautifulSoup
from time import sleep
from selenium import webdriver
import pandas as pd


fname = 'et.csv'
df = pd.read_csv(fname,header = None)
tl = list(df[0])[:3]
dfEar = pd.DataFrame(columns = ['Ticker','Date'])

driver = webdriver.Firefox()

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
    sleep(100)

dfEar.to_csv('earDateYC.csv', index = False)