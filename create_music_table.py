import os
import boto3

# Set your AWS credentials as environment variables
os.environ['AWS_ACCESS_KEY_ID'] = 'ASIAVU2WUM5AOCBSJE4E'
os.environ['AWS_SECRET_ACCESS_KEY'] = 'asIU/8HVR8U+4NB9tgj7O6zuPewnQvUW0LXO0Yif'
os.environ['AWS_SESSION_TOKEN'] = 'FwoGZXIvYXdzEN7//////////wEaDIvzHVrwLtCq/Df5CSLNASZ41XGpkz2uN598N/ZuolcG6KWeFnGKc+QNJeZd0xeraen6lWDZFBd8APUJI7I2gRV+5VNOy7v3hHXY1QkAGIHYgiXYe/4UqxT6gRPO3HFjggFdNlBNYN0LdGhTwiuY2Zui+fO41H12KaCDq6C6XiJ1hWZUrcTccPIXuNE7bgGKzYUwWopIRFARk6OFyOSMiZmngkfUZ0CK9AIx10oYiAiEDXtJjpLD970Sr8c2m30NxfiSS7WFkHCZNBLslL9juqyDKekogRG3pFND+30o+9vYoQYyLU2pIyQpjT4AXiBCcrEfiLdmlK1GK9dM6PTZOjojaxuuiDPeDWN9qECbfgpJiQ=='  # Optional if you are using temporary credentials

# Initialize the DynamoDB client
dynamodb = boto3.resource('dynamodb', region_name='us-east-1')

# Create the "music" table
table = dynamodb.create_table(
    TableName='music1',
    KeySchema=[
        {
            'AttributeName': 'title',
            'KeyType': 'HASH'
        },
        {
            'AttributeName': 'artist',
            'KeyType': 'RANGE'
        }
    ],
    AttributeDefinitions=[
        {
            'AttributeName': 'title',
            'AttributeType': 'S'
        },
        {
            'AttributeName': 'artist',
            'AttributeType': 'S'
        }
    ],
    ProvisionedThroughput={
        'ReadCapacityUnits': 5,
        'WriteCapacityUnits': 5
    }
)

# Wait for the table to be created
table.meta.client.get_waiter('table_exists').wait(TableName='music')

# Print the details of the created table
print("Table status:", table.table_status)