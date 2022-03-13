from urllib.request import urlopen

import logging
import configparser
import pandas as pd
import requests

from sklearn.preprocessing import OneHotEncoder

from apscheduler.schedulers.background import BackgroundScheduler

logging.basicConfig(format="[%(asctime)s] [%(name)s] %(levelname)s: %(message)s")
logger = logging.getLogger('fmp2s3')
logger.setLevel(logging.INFO)
logger.info ("Hello from alpaca2firehose!")

config = configparser.ConfigParser()
config.read('/Users/aukermaa/.aws/alpaca2firehose')

print (config.sections())

FMP_API_KEY = config['fmp']['FMP_API_KEY']

res = requests.get(f"https://financialmodelingprep.com/api/v4/shares_float/all?apikey={FMP_API_KEY}")

df = pd.DataFrame(res.json()).set_index('symbol')

df['report_day_time'] = pd.to_datetime(df['date'])
df = df.drop(columns=['date'])

print (df)

import matplotlib.pyplot as plt
plt.hist(df['freeFloat'], bins=200, range=(0, 200))

plt.show()
