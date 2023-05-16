### The purpose of this valdation checkl is to match the current sp500 company list with what is extracted from yahoo finance. This wil lcontrol for any errors that would cause scrapy to not scrape data for a company. It will also control for companies that are removed from the index

### Import modules
import pandas as pd
import configparser 
import psycopg2
import boto3
import os

## import s3 credentials
parser = configparser.ConfigParser()
parser.read("../credentials.conf")

access_key  = parser.get("aws_boto_credentials", "access_key")
secret_key = parser.get("aws_boto_credentials", "secret_key")
region = parser.get("aws_boto_credentials", "aws_region")
bucket = parser.get("aws_boto_credentials", "bucket_name")


# Create Boto3 S3 and RDS clients
s3_client = boto3.client('s3', aws_access_key_id=access_key,
                         aws_secret_access_key=secret_key,
                         region_name=region)


# Get the most recent file in the S3 bucket
most_recent_file = max(response['Contents'], key=lambda x: x['LastModified'])
most_recent_file_key = most_recent_file['Key']

# Download the most recent file from S3
file_path =  os.path.basename(most_recent_file_key)

s3_client.download_file(bucket, most_recent_file_key, file_path)

extracted_tickers = pd.read_csv(file_path, usecols=['Ticker'])