#!/bin/bash
wget https://earn-dt.s3.amazonaws.com/et.csv
wget https://earn-dt.s3.amazonaws.com/edate.csv
wget https://www.sec.gov/include/ticker.txt
#cat et.csv
# pull the earnings data from yc
# temporarily commenting out the yc scraper
#python ed.py
python ear8ksec.py
# tag the data with Before, After, or leave blank
# calculate the effective earn date
#cat earDateYC.csv