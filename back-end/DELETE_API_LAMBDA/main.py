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

    #now = datetime.now()
    #dynamodb_res = boto3.resource('dynamodb', region_name = 'eu-central-1')
    #table_name = os.environ['TABLE_NAME']
    
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
    
    #print(event)
    line_to_add = json.loads(event['body'])
    #print(line_to_add)
    LOCAL_FILE = '/tmp/test.txt'
    
    
    
    #convert_to_datetime = datetime.strptime(line_to_add['Vacation Date'],'%d/%m/%Y')
       
    vacation_date = line_to_add['DateOfAbsence']
    #vacation_date = json.dumps(convert_to_datetime)
    EmployeeID = line_to_add['EmployeeID']
    table_id = line_to_add['id']
    code_leave_reason = line_to_add['AbsenceTypeCode']
    rating = {}
    #leave_reason = json.dumps(line_to_add['Leave Reason'])
    status = line_to_add['Status']
    #table = dynamodb_res.Table(table_name)
    
        
    item = {
        "id": table_id
    }
    
    '''
    try:
        obj=s3.Bucket(s3_bucket_name).download_file(LOCAL_FILE, s3_key_website)
    except ClientError as e:
        if e.response['Error']['Code'] == "404":
            print("The object does not exist.")
        else:
            raise
    with open('/tmp/test.txt', 'a') as fd:
        fd.write(item)


    s3.meta.client.upload_file(LOCAL_FILE, s3_bucket_name, s3_key_website)...
    '''
    
    
    
    local_data = item
    
    
    resp=s3_c.get_object(Bucket=s3_bucket_name, Key=s3_key_website)
    data=resp.get('Body')
    
    json_data = json.load(data)
    #print(json_data)
    id_to_append = []
    counter = 1
    for i in json_data:
        if i['id'] != local_data['id']:
            i['id'] = counter
            id_to_append.append(i)
            counter = counter + 1
            
    #print(json_data)
    s3_c.put_object(Bucket=s3_bucket_name, Key=s3_key_website, Body=json.dumps(id_to_append).encode('UTF-8'))
    
    
    #s3_c.put_object( Body=(bytes(json.dumps(item).encode('UTF-8'))), ContentType='application/json',Bucket=s3_bucket_name ,Key=s3_key_website )
    #( Body=(bytes(json.dumps(json_data).encode('UTF-8'))), ContentType='application/json' )
        
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
    
  
    
