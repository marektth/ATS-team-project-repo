import json
import boto3
import os
import boto3
from botocore.exceptions import ClientError
from datetime import datetime

s3_c = boto3.client('s3')

s3_bucket_name = os.environ.get('BUCKET_NAME')
s3_key_website = os.environ.get('OBJECT_NAME')


def lambda_handler(event, context):

   
    s3 = boto3.resource('s3')
    
    try:
        s3.Object(s3_bucket_name, s3_key_website).load()
    except botocore.exceptions.ClientError as e:
        if e.response['Error']['Code'] == "404":
            print(f"File ({s3_key_website})) required by this function does not exist!")
            return f"File ({s3_key_website})) required by this function does not exist!"
        else:
            raise f"File ({s3_key_website}) required by this function is not accessible!"
            print(f"File ({s3_key_website}) required by this function is not accessible!")
            return f"File ({s3_key_website}) required by this function is not accessible!"
    
  
    line_to_add = json.loads(event['body'])
   
    
    
       
    vacation_date = line_to_add['DateOfAbsence']
    EmployeeID = line_to_add['EmployeeID']
    table_id = 0
    code_leave_reason = line_to_add['AbsenceTypeCode']
    rating = {}
    leave_reason = line_to_add['LeaveReason']
    status = line_to_add['Status']
  
    
        
    item = {
        "id": table_id,
        "EmployeeID": EmployeeID,
        "DateOfAbsence": vacation_date,
        "AbsenceTypeCode": code_leave_reason,
        "Status": status,
        "LeaveReason": leave_reason,
        "Rating": rating
    }
    
  
    
    local_data = item
    
    
    resp=s3_c.get_object(Bucket=s3_bucket_name, Key=s3_key_website)
    data=resp.get('Body')
    
    json_data = json.load(data)
    
    
    counter = 1
    for i in json_data:
        i['id'] = counter
        counter = counter + 1
            
    local_data['id'] = counter
    json_data.append(local_data)
    print(json_data)
    s3_c.put_object(Bucket=s3_bucket_name, Key=s3_key_website, Body=json.dumps(json_data,indent=4).encode('UTF-8'))
   
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
    
  
    
