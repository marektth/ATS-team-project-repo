import json
from pprint import pprint
import boto3
import botocore
from botocore.exceptions import ClientError
import os
import pandas as pd

s3_c = boto3.client('s3')

s3_bucket_name = os.environ.get('BUCKET_NAME')
s3_key_website_absence = os.environ.get('OBJECT_NAME_ABSENCE')
s3_key_website_teams = os.environ.get('OBJECT_NAME_TEAMS')
s3_key_website_employees = os.environ.get('OBJECT_NAME_EMPLOYEES')
s3_key_website_jobs = os.environ.get('OBJECT_NAME_JOBS')

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
            
def load_table(s3_bucket_name, s3_key_website):
    resp=s3_c.get_object(Bucket=s3_bucket_name, Key=s3_key_website)
    data=resp.get('Body')
    return json.load(data)


def lambda_handler(event, context):
    
    permission_testing(s3_bucket_name, s3_key_website_absence)
    
    manager_id = int(event["queryStringParameters"]['managerID'])
    
    absence_data = load_table(s3_bucket_name, s3_key_website_absence)
    employees = load_table(s3_bucket_name, s3_key_website_employees)
    teams = load_table(s3_bucket_name, s3_key_website_teams)
    jobs = load_table(s3_bucket_name, s3_key_website_jobs)
    
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
        absence_data = pd.DataFrame(absence_data)
        employees = pd.DataFrame(employees)
        teams = pd.DataFrame(teams)
        jobs = pd.DataFrame(jobs)
        
        ouids = teams.loc[teams['ManagerID'] == manager_id]["OUID"].values
        response_data = []
        for ouid in ouids:
            ou_employees_ids = employees.loc[employees['OUID'] == ouid]["EmployeeID"].values
            ou_absence_data = absence_data[absence_data['EmployeeID'].isin(ou_employees_ids)]
            ou_absence_data = pd.merge(ou_absence_data, employees, on = 'EmployeeID', how = 'left')
            if not ou_absence_data.empty:
                ou_absence_data = pd.merge(ou_absence_data, jobs, left_on = 'EmploymentNumber', right_on = 'id', how = 'left')
                ou_absence_data = ou_absence_data.drop(['Rating', 'OUID', 'LeaveBalance', 'MinRequirement', 'id_y'], axis = 1)
                ou_absence_data = ou_absence_data.rename(columns={"id_x": "id"})
            ou_data_dict = {
                "OUID": ouid,
                "OUName" : teams.loc[teams['OUID'] == ouid]["TeamName"].values[0],
                "Data": ou_absence_data if not ou_absence_data.empty else None
            }
            response_data.append(ou_data_dict.copy())
        
        response_data_df = pd.DataFrame(response_data)
    
    except ClientError as e:
        response['body'] = e.response['Error']['Message']
        return response
    else:
        response['body'] = response_data_df.to_json(orient="records")
        return response
