import scrapy
import pandas as pd
import csv
from datetime import date

# df = pd.read_csv('/Data/company_info.csv' , usecols=['Ticker'])
# ticker_list = list(df['Ticker'])
# url_list = []

# for i in ticker_list:
#      url_list.append(f'https://finance.yahoo.com/quote/{i}?p={i}')


class stockPrices(scrapy.Spider):
    name = 'historical_data'

    start_urls = ['https://finance.yahoo.com/quote/AMZN/history?period1=1652832000&period2=1684368000&interval=1d&filter=history&frequency=1d&includeAdjustedClose=true'] #url_list

    def parse(self, response):
         

         response.url