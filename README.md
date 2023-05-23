# SP 500 Stock Price Pipeline

The purpose of this project was to build an automated data pipeline that extracts daily stock prices from Yahoo Finance and store them into a AWS RDS Postres database. The data is then used to create dashdboards in Power BI  to extract insights. The data is processed in batches everyday Monday to Friday as a csv file and saved in an Amazon S3 Bucket and then loaded into the database from the S3 bucket. The whole process is automated in Apache Airflow. 
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

## File Contents 
    airflow
    database
      Data
           Contains the orignal company info and the data used to create the dimension tables in the database
                 company_info.csv
                 company_dimension.csv
                 industry_dimension.csv
                 sector_dimension.csv
      postgres_scripts
            Contains the sripts used to create the fact and dimension tab;es
                  dimension_tables_creation.sql
                  fact_table_creation_script.sql
            
    extraction
      company information 
            company_info.ipynb
                  Code used to extract the infomration about each company
            urls_list.ipynb
                  Code used to test creating the URLs needed for extraction
      historical_data
            Data
            historical_data
                  This folder is the scrapy porject created to scrape historical data on each company. Please use this file path to see the script actually used to do the webscraping: spiders -> main.py   
      stock_data
            stock_data
                  This folder is the scrapy project used to extract daily stock data. The script serves as the extraction phase of the pipeline
                  
    load 
      s3_to_rds.py
    validation_Tests
      testing ground
      ticker_check.py
## Source System 
   ### The source system for the stock data is Yahoo Finance (https://finance.yahoo.com/). Yahoo finance, continually updates stock prices in real time until market close at 4:00pm. Here you can find a summary showing the open and close prices, volume, average volume, bid and ask spreads, the days range and much more. They also have tabs where you can use interactive charts to analyze a given stock and tabs that show more statistics and historical data. For our purposes, we only need to be concerned with the sumnmary page. This tab has all the information that we are going to scrape from the website: ticker, open price , closing price, day's range, and volume
## Ingestion
 ### Extraction
   ###      I used a batch processing method that gets the data for each stock after the market closes. Once the data for every company is collected, the batch is loaded into a S3 bucket as a csv file. 
   ###      In order to achieve this I employed a python module called Scrapy. Scrapy is a webscraping module that uses css selectors to get elements from the underlying html file that powers a web page. I also needed a way to get to the webpage of each company on the sp500. I was able to do this by having my script dynamically change the url to scrape. Here is an example url: https://finance.yahoo.com/quote/AAPL?p=AAPL&.tsrc=fin-srch. As you can see the ticker symbol appears twice in the url. What I did was iterate through a list of tickers creating the url shown above for each ticker. The web scraping script then scrapes each url; appending a csv file with each companies data. Once all the urls are scraped, the csv file is loaded to the S3 bucket.
   ### Load 
## Transform 
## Validation Tests
## Orchestration Metrics 
  ### Pipeline Performance
  ### Validation Poerformance
## Limitations

    
      
