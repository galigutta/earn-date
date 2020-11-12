#!/bin/bash
wget https://earn-dt.s3.amazonaws.com/et.csv
git pull origin main
cat et.csv
python ed.py
cat earDateYC.csv