import json
import boto3
import os
from datetime import datetime




def lambda_handler(event, context):

    
    #s3_client = boto3.client('s3')
    now = datetime.now()
    dynamodb = boto3.client('dynamodb')
    dynamodb_res = boto3.resource('dynamodb', region_name = 'eu-central-1')
    TableName = os.environ['TABLE_NAME']
    
#  "httpMethod": "POST",    
#    if event.htttpMethod == POST
#       save to dynamoDB
#     else:
#         return json format
    #line_to_check = event['httpMethod']
    #method_test = json.dumps(line_to_check['access-control-request-method'])
    
    #print(line_to_check)
    
    #if event['headers']['access-control-request-method'] == 'POST':
    #print(event['headers']['access-control-request-method'])
    print(event)
    line_to_add = json.loads(event['body'])
    print(line_to_add)
    #print("THIS IS BEING ADDED")
    #print(line_to_add)
        
    #print(event['httpMethod'])     
    
    actual_date = json.dumps(line_to_add['dateOfRequest'])
    person_num = json.dumps(line_to_add['Person_Number'])
    date_time = now.strftime("%m/%d/%Y, %H:%M:%S")+"_"+person_num
    code_leave_reason = json.dumps(line_to_add['codeLeaveReason'])
    start_date = json.dumps(line_to_add['startDate'])
    end_date = json.dumps(line_to_add['endDate'])
    leave_reason = json.dumps(line_to_add['leaveReason'])
    status = json.dumps(line_to_add['status'])
    table = dynamodb_res.Table(TableName)
        
    #print(name)
    #print(surname)
    #print(age)
        
    Item = {
        "id": date_time,
        "dateOfRequest": actual_date,
        "Person_Number": person_num,
        "startDate": start_date,
        "endDate": end_date,
        "codeLeaveReason": code_leave_reason,
        "leaveReason": leave_reason,
        "status": status
    }
        
    table.put_item(Item=Item)
        
    response = {
        "statusCode": 200,
        "headers": {
            'Access-Control-Allow-Headers': 'Content-Type',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'OPTIONS,POST,GET'
        },
        "body": json.dumps("WRITTEN")
    }
    
    return response
    
  
    
