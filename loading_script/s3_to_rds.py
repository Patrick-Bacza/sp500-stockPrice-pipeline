import boto3
import configparser
import psycopg2
import configparser

parser = configparser.ConfigParser()
parser.read("credentials.conf")
db_name = parser.get("aws_rds_credentials", "rds_db_name")
username = parser.get("aws_rds_credentials", "rds_username")
password = parser.get("aws_rds_credentials", "rds_password")
host = parser.get("aws_rds_credentials", "rds_host")
port = parser.get("aws_rds_credentials", "rds_port")

access_key  = parser.get("aws_boto_credentials", "access_key")
secret_key = parser.get("aws_boto_credentials", "secret_key")
region = parser.get("aws_boto_credentials", "aws_region")




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

# # List objects in the S3 bucket
# response = s3_client.list_objects_v2(Bucket=S3_BUCKET_NAME)

# # Get the most recent file in the S3 bucket
# most_recent_file = max(response['Contents'], key=lambda x: x['LastModified'])
# most_recent_file_key = most_recent_file['Key']

# # Download the most recent file from S3
# file_path = '/tmp/' + os.path.basename(most_recent_file_key)
# s3_client.download_file(S3_BUCKET_NAME, most_recent_file_key, file_path)

# # Load the file into the PostgreSQL database
# with open(file_path, 'r') as file:
#     cursor = rds_conn.cursor()
#     cursor.copy_from(file, 'your_table_name', sep=',')  # Assuming a CSV file with comma-separated values
#     rds_conn.commit()
#     cursor.close()

# # Clean up - Delete the downloaded file
# os.remove(file_path)

# # Close the RDS connection
# rds_conn.close()