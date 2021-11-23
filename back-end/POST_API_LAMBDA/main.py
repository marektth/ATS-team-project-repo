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
       
    vacation_date = json.dumps(line_to_add['Vacation Date'])
    EmployeeID = json.dumps(line_to_add['Employee ID'])
    date_time = now.strftime("%m/%d/%Y, %H:%M:%S")+"_"+EmployeeID
    code_leave_reason = json.dumps(line_to_add['Code Leave Reason'])
    leave_reason = json.dumps(line_to_add['Leave Reason'])
    status = json.dumps(line_to_add['Status'])
    table = dynamodb_res.Table(table_name)
        
    item = {
        "id": date_time,
        "Vacation Date": vacation_date,
        "Employee ID": EmployeeID,
        "Code Leave Reason": code_leave_reason,
        "Leave Reason": leave_reason,
        "Status": status
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
    
  
    
