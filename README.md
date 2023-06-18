# SP 500 Stock Price Pipeline

The purpose of this project was to build an automated data pipeline that extracts daily stock prices from Yahoo Finance and store them in an AWS RDS Postgres database. The data is then used to create dashdboards in Power BI to extract insights. The data is processed in batches everyday Monday to Friday as a csv file and saved in an Amazon S3 Bucket and then loaded into the database from the S3 bucket. The whole process is automated in Apache Airflow. 
## Table of Contents

## Technologies Used

1. Python 
      Scrapy - Web scraping library used to extract data from Yahoo Finance
      Pandas
      Psycopg2 - POstgreSQL adapter
      boto3 - Module used for interacting with the AWS S# bucket and AWS relational database
      configparser - Module used for interacting with config files
2. SQL
3. Apache Airflow
4. Power BI
5. Amazon Web Services
      S3 Bucket
      RDS PostgeSQL


## Source System 
   ###      The source system for the stock data is Yahoo Finance (https://finance.yahoo.com/). Yahoo finance, continually updates stock prices in real time until after market trading hours stops at 8:00pm. Here you can find a summary showing the open and close prices, volume, average volume, bid and ask spreads, the days range and much more. They also have tabs where you can use interactive charts to analyze a given stock and tabs that show more statistics and historical data. For our purposes, we only need to be concerned with the summary page. This tab has all the information that we are going to scrape from the website: ticker, open price , closing price, day's range, and volume.
## Database
   ### I used an AWS PostgreSQL RDS as my database. It is a simple database with 3 dimensional tables: 1. Sectors - List of Sectors 2. Industries - List of Industries 3. Company dimension - Lists the ticker symbol, company name , sector ID and Industry ID and one fact table for the daily stock price data.
   
## Ingestion
 ### Extraction
   ###      I treat each trading day as a batch. After hours trading ends at 8:00pm and my pipeline is scheduled to start at 8:05pm. Once the data for every company is collected, the batch is loaded into a S3 bucket as a csv file. 
   ###      In order to achieve this I employed a python module called Scrapy. Scrapy is a webscraping module that uses css selectors to get elements from the underlying html file that powers a web page. I needed a way to get to the webpage of each company on the sp500. I was able to do this by having my script dynamically change the url to scrape. Here is an example url: https://finance.yahoo.com/quote/AAPL?p=AAPL&.tsrc=fin-srch. As you can see the ticker symbol appears twice in the url. What I did was iterate through a list of tickers creating the url shown above for each ticker. The web scraping script then scrapes each url; appending a csv file with each companies data. Once all the urls are scraped, the csv file is loaded to the S3 bucket.
 ### Validation Test 
 ###        Once the data has been extracted and loaded to the S3 bucket, a validation test is run to ensure that data was extracted for each company in the dataset. The test runs by pulling the most recent file from S3 and reading in the ticker symbols from the dataset as well as reading in the ticker symbols currently in the database. The test then matches the two lists together, If the lists match, the test passses and the task that moves the data from S3 to the RDS starts. If the lists do not match, the test throws an exception error and halts the pipeline. The error messaage will then tell you which ticker symbols were not extracted from yahoo finance. additionally, an email is sent notifying me that the test has failed. 
   ### Load 
   ###       Once the validation test passes, a python script is used to connect to the S3 bucket and extract the most recent file added to the bucket. It then imports the data in the stock data RDS.
## Transform 
   ### I used Power BI as my visualization software to transform, visualize and serve the stock data. I created three separate views of the data:
   ###      1. 
   ###      2. Snapshot of top gainers/losers
   ###      3. Single stock dashboard
   ###      4. Industry dashboard

## Orchestration Metrics 
  ### Pipeline Performance
  ### Coming Soon
  ### Validation Poerformance
  ### Coming Soon
### Limitations
  ##        The SP500 can and does remove and add companies infrequently throughout the year. For Example, Silicon Valley Bank was removed when it collapsed. Currently I do not have a way to automatically check and handle this. I have to periodically check the SP500 website for these updates and then manually add the companies to the database. Furthermore, I then have to run a data extraction script to get the historical data for any added companies. 
## Further Enhancements
   ### The S&P 500 index periodically removes and adds companies to the index. The pipeline currently doesn't have the functionality to automatically take care of this. I have to manually add any new companies added to the index. Currently, the only way to find out about additions and subtractions is by waiting for statements from the index. In the future, I would liek to find a way to automate handling slowly changing dimensions.


    
      
