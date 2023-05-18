### The purpose of this validation check is to match the current sp500 company list with what is extracted from yahoo finance. This will control for any errors that would cause scrapy to not scrape data for a company.

### Import modules
import pandas as pd
import configparser 
import psycopg2
import boto3
import os

## import s3 credentials
parser = configparser.ConfigParser()
parser.read("/mnt/c/Users/Patrick/documents/projects/sp500-stockPrice-pipeline/credentials.conf")

access_key  = parser.get("aws_boto_credentials", "access_key")
secret_key = parser.get("aws_boto_credentials", "secret_key")
region = parser.get("aws_boto_credentials", "aws_region")
bucket = parser.get("aws_boto_credentials", "bucket_name")


# Create Boto3 S3 and RDS clients
s3_client = boto3.client('s3', aws_access_key_id=access_key,
                         aws_secret_access_key=secret_key,
                         region_name=region)

# List objects in the S3 bucket
response = s3_client.list_objects_v2(Bucket=bucket)



# Get the most recent file in the S3 bucket
most_recent_file = max(response['Contents'], key=lambda x: x['LastModified'])
most_recent_file_key = most_recent_file['Key']

# Download the most recent file from S3
file_path =  os.path.basename(most_recent_file_key)

s3_client.download_file(bucket, most_recent_file_key, file_path)

extracted_tickers = pd.read_csv(file_path, usecols=['Ticker'])

### read in csv with tickers currently in database

tickers_df = pd.read_csv('/mnt/c/Users/Patrick/Documents/Projects/sp500-stockPrice-pipeline/database/Data/company_info.csv' , usecols=['Ticker'])


### Create two sets. One with the tickers from the daily extraction and one with the tickers from the database
extracted_set = set(extracted_tickers['Ticker'])

tickers_list_set = set(tickers_df['Ticker'])



 
difference = tickers_list_set.difference(extracted_set)




os.remove(file_path)

if tickers_list_set != extracted_set:
    raise Exception(f"Ticker validation failed: Lists do not match: {difference}")