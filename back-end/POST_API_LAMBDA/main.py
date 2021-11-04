import json
import boto3
import os
from datetime import datetime




def lambda_handler(event, context):

    now = datetime.now()
    dynamodb_res = boto3.resource('dynamodb', region_name = 'eu-central-1')
    table_name = os.environ['TABLE_NAME']
    
    print(event)
    line_to_add = json.loads(event['body'])
    print(line_to_add)
       
    actual_date = json.dumps(line_to_add['dateOfRequest'])
    person_num = json.dumps(line_to_add['Person_Number'])
    date_time = now.strftime("%m/%d/%Y, %H:%M:%S")+"_"+person_num
    code_leave_reason = json.dumps(line_to_add['codeLeaveReason'])
    start_date = json.dumps(line_to_add['startDate'])
    end_date = json.dumps(line_to_add['endDate'])
    leave_reason = json.dumps(line_to_add['leaveReason'])
    status = json.dumps(line_to_add['status'])
    table = dynamodb_res.Table(table_name)
        
    item = {
        "id": date_time,
        "dateOfRequest": actual_date,
        "Person_Number": person_num,
        "startDate": start_date,
        "endDate": end_date,
        "codeLeaveReason": code_leave_reason,
        "leaveReason": leave_reason,
        "status": status
    }
        
    table.put_item(Item=item)
        
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
    
  
    
