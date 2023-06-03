import scrapy
import pandas as pd
import csv
from datetime import date

df = pd.read_csv('/Data/company_info.csv' , usecols=['Ticker'])
ticker_list = list(df['Ticker'])
url_list = []

for i in ticker_list:
    url_list.append(f'https://finance.yahoo.com/quote/{i}/history?period1=1671753600&period2=1671840000&interval=1d&filter=history&frequency=1d&includeAdjustedClose=true')


class stockPrices(scrapy.Spider):
    name = 'historical_data'

    start_urls =  url_list

    def parse(self, response):
         
        with open('Dec232022Correction.csv', 'a', newline='') as csvfile:
            writer = csv.writer(csvfile)

            rows = response.css('table[data-test="historical-prices"] tr')

            for row in rows:
                cells = row.css('td')
                data = []
                for cell in cells:
                    cell_text = cell.css('span::text').get()
                    data.append(cell_text)
                data.append(response.css('div#quote-header-info fin-streamer[data-field="regularMarketPrice"]::attr(data-symbol)').get())
                writer.writerow(data)
