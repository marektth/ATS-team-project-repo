import json
from pprint import pprint
import boto3
from botocore.exceptions import ClientError
import os
import pandas as pd

s3_c = boto3.client('s3')

s3_bucket_name = os.environ.get('BUCKET_NAME')
s3_key_website_absence = os.environ.get('OBJECT_NAME_ABSENCE')
s3_key_website_employees = os.environ.get('OBJECT_NAME_EMPLOYEE')

def load_table(s3_bucket_name, s3_key_website):
    resp=s3_c.get_object(Bucket=s3_bucket_name, Key=s3_key_website)
    data=resp.get('Body')
    return json.load(data)
    
def permission_testing(s3_bucket_name, s3_key_website):
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


def lambda_handler(event, context):
    
    permission_testing(s3_bucket_name, s3_key_website_absence)
    
    employee_id = int(event["queryStringParameters"]['personID'])
    
    absence_data = load_table(s3_bucket_name, s3_key_website_absence)
    employees = load_table(s3_bucket_name, s3_key_website_employees)
    
    response = {
            "statusCode": 200,
            "headers": {
                'Access-Control-Allow-Headers': 'Content-Type',
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'OPTIONS,POST,GET'
            },
            "body": ""
    }
    
    try:
        # load data
        absence_data = pd.DataFrame(absence_data)
        employees = pd.DataFrame(employees)
        
        # get only specified employee data
        absence_data_employee = absence_data.loc[absence_data['EmployeeID'] == employee_id]
        employee_data = employees.loc[employees['EmployeeID'] == employee_id]
        
        response_data = [{    
            "AbsenceData" : absence_data_employee,
            "EmployeeData" : employee_data
            }]
        response_data_df = pd.DataFrame(response_data)
        
  
    except ClientError as e:
        response['body'] = e.response['Error']['Message']
        return response
    else:
        response['body'] = response_data_df.to_json(orient="records")
        return response
