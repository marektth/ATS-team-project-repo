import json
from pprint import pprint
import boto3
from botocore.exceptions import ClientError
import os
import pandas as pd

def lambda_handler(event, context):
    # TODO implement
    
    #print(event)
    
    employeeID = event["queryStringParameters"]['personID']
    
    dynamodb = boto3.resource('dynamodb')
    table_name = os.environ['TABLE_NAME']
    table = dynamodb.Table(table_name)
    list_to_return = []
    try:
        x = table.scan()
        #print(x)
        df = pd.json_normalize(x['Items'])
        #print(df['EmployeeID'])
        return_data = df.index[df['Employee ID'] == employeeID].tolist()
        #list_to_return.append(df['EmployeeID'][return_data][0])
        list_to_return = df.iloc[return_data]
        list_to_return = df.to_json(orient="split")
        parsed = json.loads(list_to_return)
        print(parsed)
        
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
        "body": json.dumps(parsed)
        }
        
        return response
    
    
    
    return response
