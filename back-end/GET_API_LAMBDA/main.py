import json
from pprint import pprint
import boto3
from botocore.exceptions import ClientError
import os

s3 = boto3.client('s3')

s3_bucket_name = os.environ.get('BUCKET_NAME')
s3_key_website = os.environ.get('OBJECT_NAME')
s3_key_website_employee = os.environ.get('OBJECT_NAME_EMPLOYEE')


def lambda_handler(event, context):
    # TODO implement
    
    employee_id = event["queryStringParameters"]['personID']
    s3 = boto3.resource('s3')
    
    try:
        s3.Object(s3_bucket_name, s3_key_website).load()
    except botocore.exceptions.ClientError as e:
        if e.response['Error']['Code'] == "404":
            print(f"File ({s3_key_website})) required by this function does not exist!")
            return f"File ({s3_key_website})) required by this function does not exist!"
        else:
            print(f"File ({s3_key_website}) required by this function is not accessible!")
            raise e
    try:
       
        obj = s3.Object(s3_bucket_name, s3_key_website)
        data = obj.get()['Body'].read().decode('utf-8')
        return_data = []
        return_data_employee = []
       
        if employee_id == "all":
            json_data = json.loads("" + 
            data.replace("}\n{", "},\n{") + 
            "")
            return_data.append(json_data)
   
        json_data = json.loads("" + 
            data.replace("}\n{", "},\n{") + 
            "")
        
        
        obj_employee = s3.Object(s3_bucket_name, s3_key_website_employee)
        data_employee = obj_employee.get()['Body'].read().decode('utf-8')
        return_data_employee = []
        
        if employee_id == "all":
            json_data_employee = json.loads("" + 
            data_employee.replace("}\n{", "},\n{") + 
            "")
            return_data_employee.append(json_data_employee)
   
        json_data_employee = json.loads("" + 
            data_employee.replace("}\n{", "},\n{") + 
            "")
        
        
      
        for index in range (len(json_data)):
            if str(json_data[index]['EmployeeID']) == employee_id:
                json_data[index]['EmployeeID'] = employee_id
                return_data.append(json_data[index])
        
    
        return_data_employee.append(next((item for item in json_data_employee if str(item["EmployeeID"]) == employee_id),None))
        
        parsed = {
          "AbsenceData" : return_data,
          "EmployeeData" : return_data_employee
        }
  
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
