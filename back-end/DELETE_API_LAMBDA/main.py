import json
import boto3
import os
import boto3
import pandas as pd
from botocore.exceptions import ClientError
from datetime import datetime
import numpy as np

s3_c = boto3.client('s3')

s3_bucket_name = os.environ.get('BUCKET_NAME')
s3_key_website = os.environ.get('OBJECT_NAME')
s3_key_website_employees = os.environ.get('OBJECT_NAME_EMPLOYEES')


def load_table(s3_bucket_name, object_key):
    resp=s3_c.get_object(Bucket=s3_bucket_name, Key=object_key)
    data=resp.get('Body')
    return pd.read_json(data)
    

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

def response_flag(return_status, s3_bucket, s3_object_absence, s3_object_employees, absence_data_param, employees_data_param):

    allow_methods = 'OPTIONS,POST,GET,DELETE'

    if(return_status == "OK"):
        if absence_data_param is not None:
            result = absence_data_param.to_json(orient="records")
            parsed = json.loads(result)
            s3_c.put_object(Bucket=s3_bucket, Key=s3_object_absence, Body=json.dumps(parsed,indent=4).encode('UTF-8'))
        if employees_data_param is not None:
            result = employees_data_param.to_json(orient="records")
            parsed_employees = json.loads(result)
            s3_c.put_object(Bucket=s3_bucket, Key=s3_object_employees, Body=json.dumps(parsed_employees,indent=4).encode('UTF-8'))
        
        

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
    elif(return_status == "NOA"):
        response = {
            "statusCode": 405,
            "headers": {
                'Access-Control-Allow-Headers': 'Content-Type',
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': allow_methods
            },
            "body": json.dumps("Not allowed !")
        }
        return response
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
        
def get_absence_hours(absence_from, absence_to, working_hours=8, date_format='%d/%m/%Y'):
    '''
        returns total leave hours of requested absence
        future feature - check if year has 356 or 366 days
    '''
    absence_from = datetime.strptime(absence_from, date_format).date()
    absence_to = datetime.strptime(absence_to, date_format).date()
    days = np.busday_count(absence_from,absence_to,weekmask=[1,1,1,1,1,0,0])
    if days > 0:
        return (days+1)*working_hours
    elif days == 0:
        return working_hours
    else:
        return 0
    

def lambda_handler(event, context):

    permission_testing(s3_bucket_name,s3_key_website)

    absence_data = load_table(s3_bucket_name, object_key=s3_key_website)
    employees_data = load_table(s3_bucket_name, object_key=s3_key_website_employees)
    
    line_to_add = json.loads(event['body'])
    request_id_to_cancel = line_to_add['id']
    date_format = '%d/%m/%Y'
    cancel_date = datetime.today().strftime(date_format)
    
    # get absence request
    request_to_cancel = (absence_data.loc[absence_data["id"] == request_id_to_cancel]).iloc[0]

    # check if request to cancel is accepted or pending
    if request_to_cancel['Status'] == "Pending":
        # if pending change status to cancelled 
        # do not change column AbsenceTo
        absence_data.loc[absence_data['id'] == request_id_to_cancel, 'Status'] = "Cancelled"
        absence_data.loc[absence_data['id'] == request_id_to_cancel, 'StatusResolution'] = "Cancelled Pending request"
        #check if request if TIMEOFF
        did_timeoff = False
        if request_to_cancel['AbsenceTypeCode'] == "TIM":
            did_timeoff = True
            # add remaining absence hours to leave_balance of employee
            remaining_hours = get_absence_hours(request_to_cancel["AbsenceFrom"], request_to_cancel["AbsenceTo"])
            
            employee_leave_balance = (employees_data.loc[employees_data['EmployeeID']== request_to_cancel['EmployeeID']]['LeaveBalance']).values[0]
            employee_leave_balance_display = (employees_data.loc[employees_data['EmployeeID']== request_to_cancel['EmployeeID']]['LeaveBalanceDisplay']).values[0]
            
            employees_data.loc[employees_data['EmployeeID'] == request_to_cancel['EmployeeID'], 'LeaveBalance'] = employee_leave_balance + remaining_hours
            employees_data.loc[employees_data['EmployeeID'] == request_to_cancel['EmployeeID'], 'LeaveBalanceDisplay'] = employee_leave_balance_display + remaining_hours
            
        if did_timeoff:
            return response_flag("OK", s3_bucket = s3_bucket_name, s3_object_absence=s3_key_website, s3_object_employees=s3_key_website_employees, absence_data_param=absence_data, employees_data_param=employees_data)
        else:
            return response_flag("OK", s3_bucket = s3_bucket_name, s3_object_absence=s3_key_website, s3_object_employees=None, absence_data_param = absence_data, employees_data_param=None)
            
    elif request_to_cancel['Status'] == "Accepted":
        # if accepted change status to cancelled
        
        # check if not cancel_date is not past AbsenceTo
        if pd.to_datetime(request_to_cancel['AbsenceTo'], format=date_format) > pd.to_datetime(cancel_date, format=date_format):

            #check if request if TIMEOFF
            did_timeoff = False
            if request_to_cancel['AbsenceTypeCode'] == "TIM":
                did_timeoff = True
                
                # set absence_from to request AbsenceFrom is request is in future, else request has already started
                if pd.to_datetime(request_to_cancel["AbsenceFrom"], format=date_format) > pd.to_datetime(cancel_date, format=date_format):
                    absence_from = request_to_cancel["AbsenceFrom"]
                else:
                    absence_from = cancel_date
                    
                # add remaining absence hours to leave_balance of employee 
                remaining_hours = get_absence_hours(absence_from, request_to_cancel["AbsenceTo"])
                
                employee_leave_balance = (employees_data.loc[employees_data['EmployeeID']== request_to_cancel['EmployeeID']]['LeaveBalance']).values[0]
                employee_leave_balance_display = (employees_data.loc[employees_data['EmployeeID']== request_to_cancel['EmployeeID']]['LeaveBalanceDisplay']).values[0]
                employees_data.loc[employees_data['EmployeeID'] == request_to_cancel['EmployeeID'], 'LeaveBalance'] = employee_leave_balance + remaining_hours
                employees_data.loc[employees_data['EmployeeID'] == request_to_cancel['EmployeeID'], 'LeaveBalanceDisplay'] = employee_leave_balance_display + remaining_hours
                
            # set status to cancelled, change AbsenceTo to cancel_date, set StatusResolution to display user request state
            absence_data.loc[absence_data['id'] == request_id_to_cancel, 'Status'] = "Cancelled"
            if pd.to_datetime(request_to_cancel["AbsenceFrom"], format=date_format) < pd.to_datetime(cancel_date, format=date_format):
                absence_data.loc[absence_data['id'] == request_id_to_cancel, 'AbsenceTo'] = cancel_date

            absence_data.loc[absence_data['id'] == request_id_to_cancel, 'StatusResolution'] = "Cancelled Accepted request"
            if did_timeoff:
                return response_flag("OK", s3_bucket = s3_bucket_name, s3_object_absence=s3_key_website, s3_object_employees=s3_key_website_employees, absence_data_param=absence_data, employees_data_param=employees_data)
            else:
                return response_flag("OK", s3_bucket = s3_bucket_name, s3_object_absence=s3_key_website, s3_object_employees=None, absence_data_param = absence_data, employees_data_param=None)
        else:
            # if canceling is later or same as the end of absence
            return response_flag("NOA", s3_bucket = s3_bucket_name, s3_object_absence=s3_key_website, s3_object_employees=s3_key_website_employees, absence_data_param=absence_data, employees_data_param=employees_data)
    else:
        # response - cancelling not allowed on other types of statuses (Rejected, ...)
        return response_flag("NOA", s3_bucket = s3_bucket_name, s3_object_absence=s3_key_website, s3_object_employees=s3_key_website_employees, absence_data_param=absence_data, employees_data_param=employees_data)
        

    # if response OK, here save tables to S3
    # return response_flag("OK", s3_bucket = s3_bucket_name, s3_object_absence=s3_key_website, s3_object_employees=s3_key_website_employees, absence_data_param=absence_data, employees_data_param=employees_data)
   
   
    
    
    
    
     
    
    
  
    
