import json
from pprint import pprint
import boto3
from botocore.exceptions import ClientError
import os

def lambda_handler(event, context):
    # TODO implement
    
    
    dynamodb = boto3.resource('dynamodb')
    table_name = os.environ['TABLE_NAME']
    table = dynamodb.Table(table_name)

    try:
        x = table.scan()
        print(x)
    except ClientError as e:
        print()
        response = {
        "statusCode": 200,
        "headers": {
            'Access-Control-Allow-Headers': 'Content-Type',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'OPTIONS,POST,GET'
        },
        "body": e.response['Error']['Message']
        }
        
        return response
    else:
        response = {
        "statusCode": 200,
        "headers": {
            'Access-Control-Allow-Headers': 'Content-Type',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'OPTIONS,POST,GET'
        },
        "body": json.dumps(x['Items'])
        }
        
        return response
    
    
    
    return response