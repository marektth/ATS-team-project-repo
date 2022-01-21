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
s3_key_website_employee = os.environ.get('OBJECT_NAME_EMPLOYEE')

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

def get_request_leave_hours(request, working_hours=8):
        '''
            returns total leave hours of requested absence
            future feature - check if year has 356 or 366 days
        '''
        absence_from = datetime.strptime(request["AbsenceFrom"], '%d/%m/%Y').date()
        absence_to = datetime.strptime(request["AbsenceTo"], '%d/%m/%Y').date()
        days = np.busday_count(absence_from,absence_to,weekmask=[1,1,1,1,1,0,0])
        if days > 0:
            return (days+1)*working_hours
        elif days == 0:
            return working_hours
        else:
            return 0
        
def balance_evaluator(e_data, n_request, s3_bucket_name, s3_key_website_employee):

    allow_methods = 'OPTIONS,POST,GET'

    employee_leave_balance = e_data.loc[e_data['EmployeeID'] == n_request['EmployeeID']]['LeaveBalanceDisplay'].values[0]
    if n_request['AbsenceTypeCode'] == "TIM":
        if(employee_leave_balance - get_request_leave_hours(n_request) < 0):
            response = {
                "statusCode": 403,
                "headers": {
                    'Access-Control-Allow-Headers': 'Content-Type',
                    'Access-Control-Allow-Origin': '*',
                    'Access-Control-Allow-Methods': allow_methods
                },
                "body": json.dumps("Not enough leave balance for this request !")
            }
            return response
        else:
            new_leave_balance = employee_leave_balance - get_request_leave_hours(n_request)
            employee_idx = e_data[e_data['EmployeeID'] == n_request['EmployeeID']].index
            e_data.at[employee_idx, "LeaveBalanceDisplay"] = new_leave_balance
            result = e_data.to_json(orient="records")
            parsed = json.loads(result)
            s3_c.put_object(Bucket=s3_bucket_name, Key=s3_key_website_employee, Body=json.dumps(parsed,indent=4).encode('UTF-8'))
            response = {
                "statusCode": 200,
                "headers": {
                    'Access-Control-Allow-Headers': 'Content-Type',
                    'Access-Control-Allow-Origin': '*',
                    'Access-Control-Allow-Methods': allow_methods
                },
                "body": json.dumps("Leave Balance substracted.")
            }
            return response
    else:
        response = {
                        "statusCode": 200,
                        "headers": {
                            'Access-Control-Allow-Headers': 'Content-Type',
                            'Access-Control-Allow-Origin': '*',
                            'Access-Control-Allow-Methods': allow_methods
                        },
                        "body": json.dumps("OK !")
                    }
        return response


def response_flag(return_status, s3_bucket_name, s3_key_website, absence_data):
    
    allow_methods = 'OPTIONS,POST,GET'

    if(return_status == "OK"):
        result = absence_data.to_json(orient="records")
        parsed = json.loads(result)
        s3_c.put_object(Bucket=s3_bucket_name, Key=s3_key_website, Body=json.dumps(parsed,indent=4).encode('UTF-8'))
        
        response = {
            "statusCode": 200,
            "headers": {
                'Access-Control-Allow-Headers': 'Content-Type',
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': allow_methods
            },
            "body": json.dumps("Success, Written !")
        }
        return response
    # date overlap error
    elif(return_status == "DOERR"):
        response = {
            "statusCode": 403,
            "headers": {
                'Access-Control-Allow-Headers': 'Content-Type',
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': allow_methods
            },
            "body": json.dumps("Created request overlaps another request")
        }
        return response
    # end date error
    elif(return_status == "EDERR"):
        response = {
            "statusCode": 403,
            "headers": {
                'Access-Control-Allow-Headers': 'Content-Type',
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': allow_methods
            },
            "body": json.dumps("End date is in past !")
        }
        return response
    # start date error
    elif(return_status == "SDERR"):
        response = {
            "statusCode": 403,
            "headers": {
                'Access-Control-Allow-Headers': 'Content-Type',
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': allow_methods
            },
            "body": json.dumps("Start date is in past !")
        }
        return response
    # date range error
    elif(return_status == "DRERR"):
        response = {
            "statusCode": 403,
            "headers": {
                'Access-Control-Allow-Headers': 'Content-Type',
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': allow_methods
            },
            "body": json.dumps("Start date is later End date !")
        }
        return response
    # employee not in database error
    elif(return_status == "EMERR"):
        response = {
            "statusCode": 403,
            "headers": {
                'Access-Control-Allow-Headers': 'Content-Type',
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': allow_methods
            },
            "body": json.dumps("Employee does not exist !")
        }
        return response
    # generic error
    else:
        response = {
            "statusCode": 404,
            "headers": {
                'Access-Control-Allow-Headers': 'Content-Type',
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': allow_methods
            },
            "body": json.dumps("Error !")
        }
        return response
    
    

def lambda_handler(event, context):

    permission_testing(s3_bucket_name, s3_key_website)
  
    line_to_add = json.loads(event['body'])
    absence_data = load_table(s3_bucket_name, s3_key_website)
    employee_data = load_table(s3_bucket_name, s3_key_website_employee)
    employee_data = pd.DataFrame(employee_data)
    
    # if employee id not exists
    if not ((employee_data['EmployeeID'] == int(line_to_add['EmployeeID'])).any()):
        return response_flag("EMERR", s3_bucket_name, s3_key_website, absence_data)
        
    
    date_format = '%d/%m/%Y'
    todays_date = pd.to_datetime(time(), unit='s')
    
    new_request_id = absence_data[-1]["id"] + 1
    
    
    
    new_request = {
        "id": new_request_id,
        "EmployeeID": int(line_to_add['EmployeeID']),
        "AbsenceRequestedAt": time(),
        "AbsenceFrom": line_to_add['AbsenceFrom'],
        "AbsenceTo": line_to_add['AbsenceTo'],
        "AbsenceTypeCode": line_to_add['AbsenceTypeCode'],
        "Status": line_to_add['Status'],
        "StatusResolution" : "",
        "OverlappingDays": [],
        "LeaveReason": line_to_add['LeaveReason'],
        "Rating": {}
    }
    
    
    
    
    # append to absence data table
    absence_data.append(new_request)

    # create dataframe from absence table
    absence_data = pd.DataFrame(absence_data)
    
   
    # check if request AbsenceTo is in past
    if pd.to_datetime(new_request['AbsenceTo'], format=date_format) < todays_date:
        absence_data.loc[absence_data['id'] == new_request_id, 'Status'] = "Rejected"
        absence_data.loc[absence_data['id'] == new_request_id, 'StatusResolution'] = "End date is earlier than request date"
        return response_flag("EDERR", s3_bucket_name, s3_key_website, absence_data)
        
    # check if request AbsenceFrom is in past
    elif pd.to_datetime(new_request['AbsenceFrom'], format=date_format) < todays_date:
        absence_data.loc[absence_data['id'] == new_request_id, 'Status'] = "Rejected"
        absence_data.loc[absence_data['id'] == new_request_id, 'StatusResolution'] = "Start date is later than request date"
        return response_flag("SDERR", s3_bucket_name, s3_key_website, absence_data)
        
    # check if request AbsenceFrom is not later than AbsenceTo
    elif pd.to_datetime(new_request['AbsenceTo'], format=date_format) < pd.to_datetime(new_request['AbsenceFrom'], format=date_format):
        absence_data.loc[absence_data['id'] == new_request_id, 'Status'] = "Rejected"
        absence_data.loc[absence_data['id'] == new_request_id, 'StatusResolution'] = "Start date is later End date"
        return response_flag("DRERR", s3_bucket_name, s3_key_website, absence_data)

    # in case checks before were OK, continue with:
        ## check if there are any requests with time-intervals intersecting request time-interval

    # get employee absence data
    employee_absence_data = absence_data.loc[absence_data['EmployeeID'] == new_request["EmployeeID"]]
    
    # get only accepted and pending data
    employee_absence_data = employee_absence_data[employee_absence_data['Status'].isin(["Accepted", "Pending"])]

    # check if dataframe not empty
    if not employee_absence_data.empty:

        # drop all columns except 'AbsenceFrom', 'AbsenceTo', 'id'
        employee_absence_data = employee_absence_data.loc[:, employee_absence_data.columns.isin(['id', 'AbsenceFrom', 'AbsenceTo'])]

        # format AbsenceFrom and AbsenceTo to pandas datetime in specified date format
        employee_absence_data['AbsenceFrom'] = pd.to_datetime(employee_absence_data['AbsenceFrom'], format=date_format)
        employee_absence_data['AbsenceTo'] = pd.to_datetime(employee_absence_data['AbsenceTo'], format=date_format)

        # drop new request
        request = employee_absence_data[employee_absence_data['id'] == new_request_id]
        employee_absence_data = employee_absence_data.drop(request.index)
        
        # if no data, there is only 1 request - recently created - not overlapping any other request
        if employee_absence_data.empty:
            # write data to table
            balance_check = balance_evaluator(employee_data, new_request, s3_bucket_name, s3_key_website_employee)
            if(balance_check["statusCode"] == 200):
                return response_flag("OK", s3_bucket_name, s3_key_website, absence_data)
            else:
                return balance_check


        # get nearest date to request, to filter out old data
        nearest_date = (employee_absence_data.loc[(employee_absence_data['AbsenceTo'] - \
                                    pd.to_datetime(new_request['AbsenceFrom'], format=date_format)).abs().idxmin(), 'AbsenceFrom'])
        

        # drop all absence data earlier than nearest date to request date
        employee_absence_data = employee_absence_data[employee_absence_data['AbsenceFrom'] >= nearest_date]
        
        # add recent request to check for overlaps
        employee_absence_data = employee_absence_data.append(request)
        
        # check overlapping dates
        a = np.triu(employee_absence_data['AbsenceTo'].values>=employee_absence_data['AbsenceFrom'].values[:,None])
        b = np.triu(employee_absence_data['AbsenceFrom'].values<=employee_absence_data['AbsenceTo'].values[:,None])

        # new request overlaps others Accepted or Pending
        if (employee_absence_data.shape[0] != (employee_absence_data[(a&b).sum(0)==1]).shape[0]):
            absence_data.loc[absence_data['id'] == new_request_id, 'Status'] = "Rejected"
            absence_data.loc[absence_data['id'] == new_request_id, 'StatusResolution'] = "Request timespan overlaps"
            return response_flag("DOERR", s3_bucket_name, s3_key_website, absence_data)

    #empty dataframe, no employee accepted or pending absences
    else:
        # write data to table
        balance_check = balance_evaluator(employee_data, new_request, s3_bucket_name, s3_key_website_employee)
        if(balance_check["statusCode"] == 200):
            return response_flag("OK", s3_bucket_name, s3_key_website, absence_data)
        else:
            return balance_check

    # write data to table
    balance_check = balance_evaluator(employee_data, new_request, s3_bucket_name, s3_key_website_employee)
    if(balance_check["statusCode"] == 200):
        return response_flag("OK", s3_bucket_name, s3_key_website, absence_data)
    else:
        return balance_check
    
  
    
