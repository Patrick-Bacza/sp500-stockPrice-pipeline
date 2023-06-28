import scrapy
import pandas as pd
import csv
from datetime import date




company_df =  pd.read_csv('/mnt/c/Users/Patrick/Documents/Projects/sp500-stockPrice-pipeline/database/Data/company_info.csv' , usecols=['Ticker'])
sector_df  =  pd.read_csv('/mnt/c/Users/Patrick/Documents/Projects/sp500-stockPrice-pipeline/database/Data/Indices_dimension.csv' , usecols=['Ticker'])

sector_df['Ticker'] = sector_df['Ticker'].str.replace('^' , '')

frames = [company_df , sector_df]

df = pd.concat(frames)

ticker_list = list(df['Ticker'])
url_list = []

for i in ticker_list:
    if i == 'GSPC':
        url_list.append(f'https://finance.yahoo.com/quote/%5E{i}?p=%5E{i}')

    elif 'SP500' in i:
        url_list.append(f'https://finance.yahoo.com/quote/%5E{i}?p=%5E{i}')

    else:
     url_list.append(f'https://finance.yahoo.com/quote/{i}?p={i}')

class stockPrices(scrapy.Spider):
    name = 'stock_prices'

    start_urls = url_list



    def parse(self, response):
       
        ticker = response.css('div#quote-header-info fin-streamer[data-field="regularMarketPrice"]::attr(data-symbol)').get()
        openPrice = response.css('#quote-header  td[data-test="OPEN-value"]::text').get().replace(',' ,'')
        closePrice =  response.css('div#quote-header-info fin-streamer[data-field="regularMarketPrice"]::text').get().replace(',' ,'')
        volume = response.css('#quote-header [data-field="regularMarketVolume"]::text').get().replace(',' ,'')
        #previousClose = response.css('#quote-header  td[data-test="PREV_CLOSE-value"]::text').get().replace(',' ,'')
        daysRange = response.css('#quote-header  td[data-test="DAYS_RANGE-value"]::text').get().split('-')
        low = daysRange[0].strip().replace(',' ,'')
        high = daysRange[1].strip().replace(',' ,'')
       

      


        yield {

            "Date": date.today(),
            "Ticker": ticker,
            "Open": openPrice,
            "Close": closePrice,
            "Volume": volume,
            "Intraday Low": low,
            "Intraday High": high,
            
        }


        
       