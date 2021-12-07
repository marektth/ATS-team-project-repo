import json
from pprint import pprint
import boto3
import botocore
from botocore.exceptions import ClientError
import os

s3 = boto3.client('s3')



s3_bucket_name = os.environ.get('BUCKET_NAME')
s3_key_website_absence = os.environ.get('OBJECT_NAME_ABSENCE')
s3_key_website_teams = os.environ.get('OBJECT_NAME_TEAMS')
s3_key_website_employees = os.environ.get('OBJECT_NAME_EMPLOYEES')


def lambda_handler(event, context):
    # TODO implement
    
    
    s3 = boto3.resource('s3')
    managerID = event["queryStringParameters"]['managerID']
    
    try:
        s3.Object(s3_bucket_name, s3_key_website_absence).load()
        s3.Object(s3_bucket_name, s3_key_website_teams).load()
        s3.Object(s3_bucket_name, s3_key_website_employees).load()
    except botocore.exceptions.ClientError as e:
        if e.response['Error']['Code'] == "404":
            print(f"File ({s3_key_website_absence})) required by this function does not exist!")
            return f"File ({s3_key_website_absence})) required by this function does not exist!"
        else:
            raise f"File ({s3_key_website_absence}) required by this function is not accessible!"
            print(f"File ({s3_key_website_absence}) required by this function is not accessible!")
            return f"File ({s3_key_website_absence}) required by this function is not accessible!"
        if e.response['Error']['Code'] == "404":
            print(f"File ({s3_key_website_teams})) required by this function does not exist!")
            return f"File ({s3_key_website_teams})) required by this function does not exist!"
        else:
            raise f"File ({s3_key_website_teams}) required by this function is not accessible!"
            print(f"File ({s3_key_website_teams}) required by this function is not accessible!")
            return f"File ({s3_key_website_teams}) required by this function is not accessible!"
        if e.response['Error']['Code'] == "404":
            print(f"File ({s3_key_website_employees})) required by this function does not exist!")
            return f"File ({s3_key_website_employees})) required by this function does not exist!"
        else:
            raise f"File ({s3_key_website_employees}) required by this function is not accessible!"
            print(f"File ({s3_key_website_employees}) required by this function is not accessible!")
            return f"File ({s3_key_website_employees}) required by this function is not accessible!"

    
    
    obj_absence_table = s3.Object(s3_bucket_name, s3_key_website_absence)
    data_absence_table = obj_absence_table.get()['Body'].read().decode('utf-8')
    json_data_absence = json.loads("" + 
        data_absence_table.replace("}\n{", "},\n{") + 
    "")

    obj_teams_table = s3.Object(s3_bucket_name, s3_key_website_teams)
    data_teams_table = obj_teams_table.get()['Body'].read().decode('utf-8')
    json_data_teams = json.loads("" + 
        data_teams_table.replace("}\n{", "},\n{") + 
    "")
    
    obj_employees_table = s3.Object(s3_bucket_name, s3_key_website_employees)
    data_employees_table = obj_employees_table.get()['Body'].read().decode('utf-8')
    json_data_employees = json.loads("" + 
        data_employees_table.replace("}\n{", "},\n{") + 
    "")
    
    
    ## ---- loading tables -----
    
    
    
    
    try:
        
        teams_return_data = ""
       
        
        for index in range (len(json_data_teams)):
            if str(json_data_teams[index]['ManagerID']) == managerID:
                json_data_teams[index]['ManagerID'] = managerID
                json_data_teams[index]['OUID'] = str(json_data_teams[index]['OUID'])
                teams_return_data = json_data_teams[index]['OUID']
        employees_return_data = []
        
        for index in range (len(json_data_employees)):
            if str(json_data_employees[index]['OUID']) == str(teams_return_data):
                json_data_employees[index]['EmployeeID'] = str(json_data_employees[index]['EmployeeID'])
                employees_return_data.append(json_data_employees[index]['EmployeeID'])
        return_data = []
        
        #change EmployeeID to Employee ID in this for
        for index in range (len(json_data_absence)):
            for y in range (len(employees_return_data)):
                if str(json_data_absence[index]['EmployeeID']) == employees_return_data[y]:
                    json_data_absence[index]['EmployeeID'] = str(json_data_absence[index]['EmployeeID'])
                    return_data.append(json_data_absence[index])
   
        parsed = json.dumps(return_data)
    
        
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
