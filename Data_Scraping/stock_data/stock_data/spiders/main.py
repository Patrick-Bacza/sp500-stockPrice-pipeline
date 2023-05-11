import scrapy
import pandas as pd
import csv
from datetime import date


# df = pd.read_csv('/Data/company_info.csv' , usecols=['Ticker'])
# ticker_list = list(df['Ticker'])
# url_list = []

# for i in ticker_list:
#     url_list.append(f'https://finance.yahoo.com/quote/{i}?p={i}')

class stockPrices(scrapy.Spider):
    name = 'stock_prices'

    start_urls = ['https://finance.yahoo.com/quote/GOOG?p=GOOG' , 'https://finance.yahoo.com/quote/TSLA?p=TSLA' , 'https://finance.yahoo.com/quote/META?p=META'] #url_list



    def parse(self, response):
        ticker = response.css('div#quote-header-info fin-streamer[data-field="regularMarketPrice"]::attr(data-symbol)').get()
        openPrice = response.css('#quote-header  td[data-test="OPEN-value"]::text').get()
        closePrice =  response.css('div#quote-header-info fin-streamer[data-field="regularMarketPrice"]::text').get()
        volume = response.css('#quote-header [data-field="regularMarketVolume"]::text').get().replace(',' , '')
        previousClose = response.css('#quote-header  td[data-test="PREV_CLOSE-value"]::text').get()
        daysRange = response.css('#quote-header  td[data-test="DAYS_RANGE-value"]::text').get().split('-')
        low = daysRange[0].strip()
        high = daysRange[1].strip()
        bid = response.css('[data-test="BID-value"]::text').get().split('x')
        bidPrice = bid[0].strip()
        ask = response.css('[data-test="ASK-value"]::text').get().split('x')
        askPrice = ask[0].strip()



        yield {

            "Date": date.today(),
            "Ticker": ticker,
            "Open": openPrice,
            "Close": closePrice,
            "Volume": volume,
            "Previous Close": previousClose,
            "Intraday Low": low,
            "Intraday High": high,
            "Bid": bidPrice,
            "Ask": askPrice
        }
        
       