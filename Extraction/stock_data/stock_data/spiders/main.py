import scrapy
import pandas as pd
import csv
from datetime import date




df =  pd.read_csv('/mnt/c/Users/Patrick/Documents/Projects/sp500-stockPrice-pipeline/database/Data/company_info.csv' , usecols=['Ticker'])
ticker_list = list(df['Ticker'])
url_list = ['https://finance.yahoo.com/quote/%5EGSPC?p=%5EGSPC']

for i in ticker_list:
    if i != "^GSPC":
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
        bid = response.css('[data-test="BID-value"]::text').get()
       # bidPrice = bid[0].strip().replace(',' ,'')
        ask = response.css('[data-test="ASK-value"]::text').get()
       # askPrice = ask[0].strip().replace(',' ,'')


        if ticker == '^GSPC':  # Check if the ticker is for the S&P 500 index
            bidPrice = None  # Set bid price to None
            askPrice = None  # Set ask price to None
        else:
            bidPrice = bid.split('x')[0].strip().replace(',', '') if bid else None
            askPrice = ask.split('x')[0].strip().replace(',', '') if ask else None


        yield {

            "Date": date.today(),
            "Ticker": ticker,
            "Open": openPrice,
            "Close": closePrice,
            "Volume": volume,
            "Intraday Low": low,
            "Intraday High": high,
            "Bid": bidPrice,
            "Ask": askPrice
        }


        
       