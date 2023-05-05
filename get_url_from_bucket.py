import boto3
import requests
import os

os.environ['AWS_ACCESS_KEY_ID'] = 'ASIAVU2WUM5ALVJTZUTP'
os.environ['AWS_SECRET_ACCESS_KEY'] = 'SX1N7UvvY8GqdGBzO8iWsDcn4TmqKgMWP3jJJyEb'
os.environ['AWS_SESSION_TOKEN'] = 'FwoGZXIvYXdzEH4aDLrzA+yzxpepnJSSwiLNAf2Mvd6eonJnZLucLzUTUSDBnmJKwytTmcPW4jXw1cqx0c4UicNCg80Gxth6ka8CYW9DtJDVceWQznDuAK/40FnLlzYQKSanNRrhOdmoM4ZQT72BQib58ILdrPBD1MGzOaUs3IpT3AWEecPFoA/UEkUF5jnwhU6J3qqrfw5yblAeq7uVMg4lO5xriZINbPgQYMS/yCfaohUL3sEJTblCdnbJKJLiIPWQ3LZdNcdIUxc+97Tjeg9uPxX5BI4iJMerhTOVx1wDGCM5mKuDIbIo993DoQYyLSBsky3I9tUiP0VL+L2DxIPCUiIischMTVm/Tj4yiCX6txE2x5ha9ND2I9YMsA=='  # Optional if you are using temporary credentials

# Initialize the AWS clients
dynamodb = boto3.client('dynamodb', region_name='us-east-1')
s3 = boto3.client('s3')

# Define the name of the DynamoDB table and S3 bucket
table_name = 'music'
bucket_name = 'cloudcomputingmusic'


s3_client = boto3.client('s3')
url = s3_client.generate_presigned_url(
        ClientMethod='get_object',
        Params={
            'Bucket': bucket_name,
            'Key': '#40.jpg'
        }
    )

print(url)