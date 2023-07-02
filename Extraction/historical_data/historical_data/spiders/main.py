import scrapy
import pandas as pd
import csv
from datetime import date

df = pd.read_csv('C:\\Users\\Patrick\\Documents\\Projects\\sp500-stockPrice-pipeline\\database\\Data\\Indices_dimension.csv' , usecols=['Ticker'])

df['Ticker'] = df['Ticker'].str.replace('^' , '')

ticker_list = list(df['Ticker'])
url_list = []

for i in ticker_list:
    url_list.append(f'https://finance.yahoo.com/quote/%5E{i}/history?period1=1652918400&period2=1663027200&interval=1d&filter=history&frequency=1d&includeAdjustedClose=true')

class stockPrices(scrapy.Spider):
    name = 'historical_data'

    start_urls = url_list
    def parse(self, response):
         
        with open('sectors_data_output_3.csv', 'a', newline='') as csvfile:
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
