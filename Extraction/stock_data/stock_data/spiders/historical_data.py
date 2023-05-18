import scrapy
import pandas as pd
import csv
from datetime import date

df = pd.read_csv('/mnt/c/Users/Patrick/Documents/Projects/sp500-stockPrice-pipeline/database/Data/company_info.csv' , usecols=['Ticker'])
ticker_list = list(df['Ticker'])
url_list = []

for i in ticker_list:
     url_list.append(f'https://finance.yahoo.com/quote/{i}?p={i}')


class stockPrices(scrapy.Spider):
    name = 'stock_prices'

    start_urls =  url_list