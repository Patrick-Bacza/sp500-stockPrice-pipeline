# SP 500 Stock Price Pipeline

The purpose of this project was to build an automated data pipeline that extracts daily stock prices from Yahoo Finance and store them into a AWS RDS Postres database. The data is then used to create dasboards in Power BI  to extract insights. The data is processed in batches everyday Monday to Friday as a csv file and saved in an Amazon S3 Bucket and then loaded into the database from the S3 bucket. The whole process is automated in Apache Airflow. 
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

## File Contents 
    airflow
    database
      Data 
      postgres_scripts
    extraction
      company information 
      historical_data
      stock_data
    load 
      s3_to_rds.py
    validation_Tests
      testing ground
      ticker_check.py
## Source System 
      
## Ingestion
      ### Extraction
      ### Load 
## Transform 
## Validation Tests
## Orchestration Metrics 
  ### Pipeline Performance
  ### Validation Poerformance
## Limitations

    
      
