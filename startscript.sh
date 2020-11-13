#!/bin/bash
wget https://earn-dt.s3.amazonaws.com/et.csv
wget https://www.sec.gov/include/ticker.txt
cat et.csv
# pull the earnings data from yc
python ed.py
# tag the data with Before, After, or leave blank
# calculate the effective earn date
cat earDateYC.csv