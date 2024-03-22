@echo off
set API_KEY=-api_key-
set START_DATE=2024-01-01
set END_DATE=2024-03-01
set BASE_CURRENCY=USD
set TARGET_CURRENCIES=EUR,GBP
set RESOLUTION=1d
set AMOUNT=1
set PLACES=7
set FORMAT=json

python pull_project.py
