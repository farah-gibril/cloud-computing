import boto3
import requests
import os

os.environ['AWS_ACCESS_KEY_ID'] = 'ASIAVU2WUM5AOCBSJE4E'
os.environ['AWS_SECRET_ACCESS_KEY'] = 'asIU/8HVR8U+4NB9tgj7O6zuPewnQvUW0LXO0Yif'
os.environ['AWS_SESSION_TOKEN'] = 'FwoGZXIvYXdzEN7//////////wEaDIvzHVrwLtCq/Df5CSLNASZ41XGpkz2uN598N/ZuolcG6KWeFnGKc+QNJeZd0xeraen6lWDZFBd8APUJI7I2gRV+5VNOy7v3hHXY1QkAGIHYgiXYe/4UqxT6gRPO3HFjggFdNlBNYN0LdGhTwiuY2Zui+fO41H12KaCDq6C6XiJ1hWZUrcTccPIXuNE7bgGKzYUwWopIRFARk6OFyOSMiZmngkfUZ0CK9AIx10oYiAiEDXtJjpLD970Sr8c2m30NxfiSS7WFkHCZNBLslL9juqyDKekogRG3pFND+30o+9vYoQYyLU2pIyQpjT4AXiBCcrEfiLdmlK1GK9dM6PTZOjojaxuuiDPeDWN9qECbfgpJiQ=='  # Optional if you are using temporary credentials

# Initialize the AWS clients
dynamodb = boto3.client('dynamodb', region_name='us-east-1')
s3 = boto3.client('s3')

# Define the name of the DynamoDB table and S3 bucket
table_name = 'music'
bucket_name = 'cloudcomputingmusic'

# Get all the items from the DynamoDB table
response = dynamodb.scan(TableName=table_name)

# Loop through each item and download/upload the image
for item in response['Items']:
    # Get the image URL from the item
    image_url = item['img_url']['S']
    # print(image_url)
    # Download the image data
    image_data = requests.get(image_url).content

    # # Upload the image to S3 using a unique key
    key = item['title']['S'] + '.jpg'
    s3.put_object(Bucket=bucket_name, Key=key, Body=image_data)

    # # Update the DynamoDB item with the S3 URL for the image SO THE TABLE USES THE S3 BUCKET LINK MEETING THE REQUIREMENTS
    # s3_url = f'https://{bucket_name}.s3.amazonaws.com/{key}'
    # dynamodb.update_item(
    #     TableName=table_name,
    #     Key={'title': {'S': item['title']['S']}},
    #     UpdateExpression='SET image_s3_url = :val1',
    #     ExpressionAttributeValues={':val1': {'S': s3_url}}
    # )