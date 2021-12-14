import json
import boto3
import os
import boto3
import pandas as pd
from botocore.exceptions import ClientError
from datetime import datetime
import numpy as np
from time import time

s3_c = boto3.client('s3')
s3_bucket_name = os.environ.get('BUCKET_NAME')
s3_key_website = os.environ.get('OBJECT_NAME')


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

def response_flag(return_status, s3_bucket_name, s3_key_website, absence_data):
    
    if(return_status == "OK"):
        result = absence_data.to_json(orient="records")
        parsed = json.loads(result)
        s3_c.put_object(Bucket=s3_bucket_name, Key=s3_key_website, Body=json.dumps(parsed,indent=4).encode('UTF-8'))
        response = {
            "statusCode": 200,
            "headers": {
                'Access-Control-Allow-Headers': 'Content-Type',
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'OPTIONS,POST,GET'
            },
            "body": json.dumps("Success, Written !")
        }
        return response
    elif(return_status == "NOK"):
        response = {
            "statusCode": 400,
            "headers": {
                'Access-Control-Allow-Headers': 'Content-Type',
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'OPTIONS,POST,GET'
            },
            "body": json.dumps("Something went wrong !")
        }
        return response
    else:
        response = {
            "statusCode": 404,
            "headers": {
                'Access-Control-Allow-Headers': 'Content-Type',
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'OPTIONS,POST,GET'
            },
            "body": json.dumps("Error !")
        }
        return response
    
    

def lambda_handler(event, context):

    permission_testing(s3_bucket_name, s3_key_website)
  
    line_to_add = json.loads(event['body'])
   
    
    absence_data = load_table(s3_bucket_name, s3_key_website)
    
    date_format = '%d/%m/%Y'
    todays_date = pd.to_datetime(time(), unit='s')
    
    new_request_id = absence_data[-1]["id"] + 1
    
    
    new_request = {
        "id": new_request_id,
        "EmployeeID": line_to_add['EmployeeID'],
        "AbsenceRequestedAt": time(),
        "AbsenceFrom": line_to_add['AbsenceFrom'],
        "AbsenceTo": line_to_add['AbsenceTo'],
        "AbsenceTypeCode": line_to_add['AbsenceTypeCode'],
        "Status": line_to_add['Status'],
        "StatusResolution" : "",
        "LeaveReason": line_to_add['LeaveReason'],
        "Rating": {}
    }
    
    
    
    
    
    # append to absence data table
    absence_data.append(new_request)

    # create dataframe from absence table
    absence_data = pd.DataFrame(absence_data)
    
   
    # check if request Absence timespan if its correct
    if pd.to_datetime(new_request['AbsenceTo'], format=date_format) < todays_date:
        absence_data.loc[absence_data['id'] == new_request_id, 'Status'] = "Rejected"
        absence_data.loc[absence_data['id'] == new_request_id, 'StatusResolution'] = "End date is earlier than request date"
        return response_flag("OK", s3_bucket_name, s3_key_website, absence_data)

    elif pd.to_datetime(new_request['AbsenceFrom'], format=date_format) < todays_date:
        absence_data.loc[absence_data['id'] == new_request_id, 'Status'] = "Rejected"
        absence_data.loc[absence_data['id'] == new_request_id, 'StatusResolution'] = "Start date is later than request date"
        return response_flag("OK", s3_bucket_name, s3_key_website, absence_data)

    

    # in case checks before were OK, continue:
        ## check if there are any requests with time-intervals intersecting request time-interval

    # get employee absence data
    employee_absence_data = absence_data.loc[absence_data['EmployeeID'] == new_request["EmployeeID"]]
    employee_absence_data = employee_absence_data[employee_absence_data['Status'].isin(["Accepted", "Pending"])]

    # check if dataframe not empty
    if not employee_absence_data.empty:

        # drop all columns except 'AbsenceFrom', 'AbsenceTo'
        employee_absence_data = employee_absence_data.loc[:, employee_absence_data.columns.isin(['id', 'AbsenceFrom', 'AbsenceTo'])]

        # format AbsenceFrom and AbsenceTo to pandas datetime + format to specified date format
        employee_absence_data['AbsenceFrom'] = pd.to_datetime(employee_absence_data['AbsenceFrom'], format=date_format)
        employee_absence_data['AbsenceTo'] = pd.to_datetime(employee_absence_data['AbsenceTo'], format=date_format)

        # drop new request
        request = employee_absence_data[employee_absence_data['id'] == new_request_id]
        employee_absence_data = employee_absence_data.drop(request.index)
        
        if employee_absence_data.empty:
            return response_flag("OK", s3_bucket_name, s3_key_website, absence_data)

        # get nearest date to request, to filter out old data
        nearest_date = (employee_absence_data.loc[(employee_absence_data['AbsenceTo'] - \
                                    pd.to_datetime(new_request['AbsenceFrom'], format=date_format)).abs().idxmin(), 'AbsenceFrom'])
        

        # drop all absence data earlier than nearest date to request date
        employee_absence_data = employee_absence_data[employee_absence_data['AbsenceFrom'] >= nearest_date]
        employee_absence_data = employee_absence_data.append(request)

        a = np.triu(employee_absence_data['AbsenceTo'].values>employee_absence_data['AbsenceFrom'].values[:,None])
        b = np.triu(employee_absence_data['AbsenceFrom'].values<employee_absence_data['AbsenceTo'].values[:,None])

        # new request overlaps others Accepter or Pending
        if (employee_absence_data.shape[0] != (employee_absence_data[(a&b).sum(0)==1]).shape[0]):
            absence_data.loc[absence_data['id'] == new_request_id, 'Status'] = "Rejected"
            absence_data.loc[absence_data['id'] == new_request_id, 'StatusResolution'] = "Request timespan overlaps"
            return response_flag("OK", s3_bucket_name, s3_key_website, absence_data)

    #empty dataframe, no employee absences
    else:
        return response_flag("OK", s3_bucket_name, s3_key_website, absence_data)


    # if response OK, here save table to S3

    return response_flag("OK", s3_bucket_name, s3_key_website, absence_data)
    
  
    
