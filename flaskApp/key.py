import boto3
import boto3

import os


os.environ['AWS_ACCESS_KEY_ID'] = 'ASIAVU2WUM5APLBKTF5B'
os.environ['AWS_SECRET_ACCESS_KEY'] = 'hLtQNU8p7XBpfhqNPKuucaKViqRS2RP/IaN6hBGp'
os.environ['AWS_SESSION_TOKEN'] = 'FwoGZXIvYXdzEGYaDOczseJySG09eodZwCLNATqPwQTXiGlNMiBY7gotGrcWoe3G83Ej9vlpT9UFXCtQ/AVEUMnbyhNO5YhL74pMq2Rmy1FvhHdRtD3HS6xTC8AzI5rZeBk06KlY0XKAc9LQfJEk7ZP+4Yd3Pb7ILl8ev9LNeTQMzkrMUNIOuygKJSXjAa55AvNjt8Uob9geVs0IG8l70tJKa1GEV84dsIJi467eo4OFCqEzNqfsEQDth18dQOktIB5UfgLXoYcksz8H4tgv8YiFFIJq5IKmeEp1I/lghkd+EyzlV/vhm7Yo47W+oQYyLanUpwQHm19tw/kRZk1krxCU/kmxm2eECnZxz3okuWO4Re9P9wVuw94WrVI8IA=='  # Optional if you are using temporary credentials

# Initialize the DynamoDB client
dynamodb = boto3.resource('dynamodb',region_name='us-east-1')

# Get a reference to the table
table = dynamodb.Table('music')

# Specify the partition key value and sort key value of the item to update
partition_key = 'title'
sort_key = 'artist'

# Update the item to set the sort key attribute to an empty string
table.update_item(
    Key={
        'partition-key': partition_key,
        'sort-key': sort_key
    },
    UpdateExpression='SET #sortkey = :empty',
    ExpressionAttributeNames={
        '#sortkey': 'sort-key'
    },
    ExpressionAttributeValues={
        ':empty': ''
    }
)