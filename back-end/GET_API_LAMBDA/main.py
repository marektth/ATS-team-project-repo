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
    print(employeeID)
    
    dynamodb = boto3.resource('dynamodb')
    table_name = os.environ['TABLE_NAME']
    table = dynamodb.Table(table_name)
    list_to_return = []
    try:
        x = table.scan()
        #print(x)
        df = pd.json_normalize(x['Items'])
        return_data = []
        table_list = x['Items']
        for index in range (len(table_list)):
            if str(table_list[index]['Employee ID']) == employeeID:
                table_list[index]['Employee ID'] = employeeID
                return_data.append(table_list[index])
                
        #print(df['EmployeeID'])
        #return_data = df.index[df['Employee ID'] == employeeID].tolist()       ## OG CODE..
        print(return_data)
        #list_to_return.append(df['EmployeeID'][return_data][0])
        #list_to_return = df.iloc[return_data]   ## OG CODE
        #print(list_to_return)
        #list_to_return = df.to_json(orient="split") ## OG CODE
        parsed = json.dumps(return_data)
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
        "body": parsed
        }
        
        return response
    
    
    
    return response
