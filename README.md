# SP 500 Stock Price Pipeline

###      The purpose of this project was to build an automated data pipeline that extracts daily stock prices from Yahoo Finance and store them in an AWS RDS Postgres database. The data is then used to create dashboards in Power BI to extract insights. The data is processed in batches everyday Monday to Friday as a csv file and saved in an Amazon S3 Bucket and then loaded into the database from the S3 bucket. The whole process is automated in Apache Airflow. The dashboards will be incredibly useful in analyzing price points and trends for individual stocks, the S&P 500 index and sectors. Anyone will find value from them whether they are day traders   , long term investers or casual investors.

### Below you will find the following sections:
###      Technologies Used
###      Source System
###      DAG
###      Ingestion
###            Extraction
###            Validation Test
###            Load
###      Transform
###      Limitations
###      Further Enhancements



## Technologies Used

   ###   Python 
   ###      Scrapy 
   ###      Pandas
   ###      Psycopg2 
   ###      boto3 
   ###      configparser 
   ###  SQL
   ###  Apache Airflow
   ###  Power BI
   ###  Amazon Web Services
   ###     S3 
   ###     RDS

## DAG
![image](https://github.com/Patrick-Bacza/sp500-stockPrice-pipeline/assets/120348192/b71961c3-1042-43b5-ba68-4b246fc70639)



## Source System 
   ###      The source system for the stock data is Yahoo Finance (https://finance.yahoo.com/). Yahoo finance, continually updates stock prices in real time until after market trading hours stops at 8:00pm. Here you can find a summary showing the open and close prices, volume, average volume, bid and ask spreads, the days range and much more. They also have tabs where you can use interactive charts to analyze a given stock and tabs that show more statistics and historical data. For our purposes, we only need to be concerned with the summary page. This tab has all the information that we are going to scrape from the website: ticker, open price , closing price, day's range, previous close and volume.
## Database
   ### I used an AWS PostgreSQL RDS as my database. It is a simple database with 3 dimensional tables: 1. Sectors - List of Sectors 2. Industries - List of Industries 3. Company dimension - Lists the ticker symbol, company name , sector ID and Industry ID and one fact table for the daily stock price data.

   ![image](https://github.com/Patrick-Bacza/sp500-stockPrice-pipeline/assets/120348192/169752f2-12b4-4470-92ff-0557da1beea2)

   ###  Database creation scripts:
         https://github.com/Patrick-Bacza/sp500-stockPrice-pipeline/blob/main/database/postgres_scripts/fact_table_creation%20script.sql
         https://github.com/Patrick-Bacza/sp500-stockPrice-pipeline/blob/main/database/postgres_scripts/dimension_tables_creation.sql

   
## Ingestion
 ### Extraction - https://github.com/Patrick-Bacza/sp500-stockPrice-pipeline/blob/main/Extraction/stock_data/stock_data/spiders/main.py
   ###      I treat each trading day as a batch. After hours trading ends at 8:00pm and my pipeline is scheduled to start at 8:05pm. Once the data for every company is collected, the batch is loaded into a S3 bucket as a csv file. 
   ###      In order to achieve this I employed a python module called Scrapy. Scrapy is a webscraping module that uses css selectors to get elements from the underlying html file that powers a web page. I needed a way to get to the webpage of each company on the SP500. I was able to do this by having my script dynamically change the url to scrape. Here is an example url: https://finance.yahoo.com/quote/AAPL?p=AAPL&.tsrc=fin-srch. As you can see the ticker symbol appears twice in the url. What I did was iterate through a list of tickers creating the url shown above for each ticker. The web scraping script then scrapes each url; appending a csv file with each companies data. Once all the urls are scraped, the csv file is loaded to the S3 bucket.
 ### Validation Test - https://github.com/Patrick-Bacza/sp500-stockPrice-pipeline/blob/main/Validation_Tests/ticker_check.py
 ###        Once the data has been extracted and loaded to the S3 bucket, a validation test is run to ensure that data was extracted for each company in the dataset. From time to time, the webscraper will not be able to extract value from a ticker for various reasons (ex. the webpage was reloading when the scrape sent the call). The test runs by pulling the most recent file from S3 and reading in the ticker symbols from the dataset as well as reading in the ticker symbols currently in the database. The test then matches the two lists together, If the lists match, the test passses and the task that moves the data from S3 to the RDS starts. If the lists do not match, the test throws an exception error and halts the pipeline. The error message will then tell you which ticker symbols were not extracted from yahoo finance. additionally, an email is sent notifying me that the test has failed. The test stops the pipeline in order to prevent duplicates from entering the database.
   ### Load - https://github.com/Patrick-Bacza/sp500-stockPrice-pipeline/blob/main/Load/s3_to_rds.py
   ###       Once the validation test passes, a python script is used to connect to the S3 bucket and extract the most recent file added to the bucket. It then imports the data into the RDS.
## Transform 
   ### I used Power BI as my visualization software to transform, visualize and serve the stock data. I created three separate views of the data:
   ###      1. S&P 500 Overview
   ###            The dashboard has daily trading statistics: a candle stick chart, a simple line graph with the close price, 30 day moving average and 90 day moving average and a bar chart showing the total volume. In addition to viewing the SP500 Index, you can toggle between the different sector indices as well.
   ![image](https://github.com/Patrick-Bacza/sp500-stockPrice-pipeline/assets/120348192/20441d1f-912d-4af1-ab66-681ddfb6c2d8)         
   ###      2. Snapshot of top gainers/losers
   ###             The second page shows lists of top gaining and losing stocks over different periods of time (ex. day , week , month and Year-To-Date)
   ![image](https://github.com/Patrick-Bacza/sp500-stockPrice-pipeline/assets/120348192/c2a2dc0b-6160-4323-ac60-0c09d52979f4)
   
   ###      3. Single stock dashboard
   ###              This dashboard closely mirrors the S&P 500 Index but is for the individual stocks. The only main difference is that there is a Relative Strength Index. The Relative Strength Index is a trading metric to show whether a stock is over bought or over sold. Typically, a RSI of 70 or more indicates a stock is over bought and a RSI below 20 indicates a stock is over sold.  
  ![image](https://github.com/Patrick-Bacza/sp500-stockPrice-pipeline/assets/120348192/317b9dd1-79a8-4a5c-b0d1-6824f84bc0d9)

## Orchestration Metrics 
  ### Pipeline Performance
  ### I am currently working on a dashboard that shows different metrics for the whole pipeline. I would like to see the success rate and the completion time of the pipeline over time. This way I can see if it remains consistent or starts taking longer and longer to complete
  ### Validation Performance
  ### I am also creating metrics to see how well the extraction performs. I want to see how the validation test does over time in order to know if the extraction script starts getting worse. That way I will know to investigate and fix any issues that may arise. 
## Limitations
  ###        The SP500 can and does remove and add companies infrequently throughout the year. For Example, Silicon Valley Bank was removed when it collapsed. Currently I do not have a way to automatically check and handle this. I have to periodically check the SP500 website for these updates and then manually add the companies to the database. Furthermore, I then have to run a data extraction script to get the historical data for any added companies.
## Further Enhancements
   ### The S&P 500 index periodically removes and adds companies to the index. The pipeline currently doesn't have the functionality to automatically take care of this. I have to manually add any new companies added to the index. Currently, the only way to find out about additions and subtractions is by waiting for statements from the index. In the future, I would like to find a way to automate handling these slowly changing dimensions.
   ### The stock market is also closed on Federal holidays. i hope to add functionality to the DAG that accounts for federal holidays and skips the run
   


    
      
