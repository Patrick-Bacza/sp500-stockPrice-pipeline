import boto3
import configparser
import psycopg2
import os


parser = configparser.ConfigParser()
parser.read("/mnt/c/Users/Patrick/documents/projects/sp500-stockPrice-pipeline/credentials.conf")
db_name = parser.get("aws_rds_credentials", "rds_db_name")
username = parser.get("aws_rds_credentials", "rds_username")
password = parser.get("aws_rds_credentials", "rds_password")
host = parser.get("aws_rds_credentials", "rds_host")
port = parser.get("aws_rds_credentials", "rds_port")

access_key  = parser.get("aws_boto_credentials", "access_key")
secret_key = parser.get("aws_boto_credentials", "secret_key")
region = parser.get("aws_boto_credentials", "aws_region")
bucket = parser.get("aws_boto_credentials", "bucket_name")




# Create Boto3 S3 and RDS clients
s3_client = boto3.client('s3', aws_access_key_id=access_key,
                         aws_secret_access_key=secret_key,
                         region_name=region)

rds_conn = psycopg2.connect(
    host=host,
    port=port,
    dbname= db_name,
    user=username,
    password=password
)

# List objects in the S3 bucket
response = s3_client.list_objects_v2(Bucket=bucket)

# Get the most recent file in the S3 bucket
most_recent_file = max(response['Contents'], key=lambda x: x['LastModified'])
most_recent_file_key = most_recent_file['Key']

# Download the most recent file from S3
file_path =  os.path.basename(most_recent_file_key)

print(most_recent_file)
print(most_recent_file_key)
print(file_path)
s3_client.download_file(bucket, most_recent_file_key, file_path)

# Load the file into the PostgreSQL database
with open(file_path, 'r') as file:
    next(file)
    cursor = rds_conn.cursor()
    cursor.copy_from(file, 'daily_stock_prices', sep=',' ,columns=('date' , 'ticker' , 'open_price' ,'close_price' , 'volume' , 'intraday_low' , 'intraday_high'))  # Assuming a CSV file with comma-separated values
    rds_conn.commit()
    cursor.close()

# Clean up - Delete the downloaded file
os.remove(file_path)

# Close the RDS connection
rds_conn.close()