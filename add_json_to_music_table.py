import boto3
import json
import os

# Set your AWS credentials as environment variables
os.environ['AWS_ACCESS_KEY_ID'] = 'ASIAVU2WUM5AOCBSJE4E'
os.environ['AWS_SECRET_ACCESS_KEY'] = 'asIU/8HVR8U+4NB9tgj7O6zuPewnQvUW0LXO0Yif'
os.environ['AWS_SESSION_TOKEN'] = 'FwoGZXIvYXdzEN7//////////wEaDIvzHVrwLtCq/Df5CSLNASZ41XGpkz2uN598N/ZuolcG6KWeFnGKc+QNJeZd0xeraen6lWDZFBd8APUJI7I2gRV+5VNOy7v3hHXY1QkAGIHYgiXYe/4UqxT6gRPO3HFjggFdNlBNYN0LdGhTwiuY2Zui+fO41H12KaCDq6C6XiJ1hWZUrcTccPIXuNE7bgGKzYUwWopIRFARk6OFyOSMiZmngkfUZ0CK9AIx10oYiAiEDXtJjpLD970Sr8c2m30NxfiSS7WFkHCZNBLslL9juqyDKekogRG3pFND+30o+9vYoQYyLU2pIyQpjT4AXiBCcrEfiLdmlK1GK9dM6PTZOjojaxuuiDPeDWN9qECbfgpJiQ=='  # Optional if you are using temporary credentials


# Initialize the DynamoDB client
dynamodb = boto3.resource('dynamodb', region_name='us-east-1')

# Get the existing "music" table
table = dynamodb.Table('music1')



# Update the AttributeDefinitions and ProvisionedThroughput properties
table.update(
    TableName = 'music1',
    AttributeDefinitions=[
        {
            'AttributeName': 'year',
            'AttributeType': 'N'
        },
        {
            'AttributeName': 'web_url',
            'AttributeType': 'S'
        },
        {
            'AttributeName': 'image_url',
            'AttributeType': 'S'
        }
    ],
    ProvisionedThroughput={
        'ReadCapacityUnits': 10,
        'WriteCapacityUnits': 10
    }
)

# Wait for the table to be updated
table.meta.client.get_waiter('table_exists').wait(TableName='music1')

# Print the details of the updated table
print("Table status:", table.table_status)

# Load JSON file
with open(r'C:\Users\Gibril Farah\Downloads\a1.json', 'r') as file:
    data = json.load(file)

    for item in data['songs']:
        title = item['title']
        artist = item['artist']
        year = item['year']
        web_url = item['web_url']
        img_url = item['img_url']


with table.batch_writer() as batch:
    for song in data['songs']:
        Item={
            'title': title,
            'artist': artist,
            'year': year,
            'web_url': web_url,
            'img_url': img_url
        }
        batch.put_item(Item=song)



print("Data loaded successfully into DynamoDB table.")

# import boto3

# # Create an instance of the DynamoDB client
# dynamodb = boto3.client('dynamodb', region_name='us-east-1')

# # Specify the table name
# table_name = 'music'

# # Update the table's provisioned throughput
# try:
#     response = dynamodb.update_table(
#         TableName=table_name,
#         ProvisionedThroughput={
#             'ReadCapacityUnits': 10,
#             'WriteCapacityUnits': 10
#         }
#     )
#     print("Table updated successfully:", response)
# except Exception as e:
#     print("Error updating table:", e)