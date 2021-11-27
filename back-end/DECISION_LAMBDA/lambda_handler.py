import json
import os
from numpy import empty
import pandas as pd
import datetime
import boto3
from io import StringIO


def capacity_rule(min_capacity, absence_data_accepted, absence_request, full_capacity):
    '''
        Check new request if there are overlaping dates with already accepted timeoffs...
    '''
    if(not absence_data_accepted.empty and not absence_request.empty):
        
        #converting datetime to day in year for quick number comparisions
        absence_data_accepted['DayOfYear'] =  (pd.to_datetime(absence_data_accepted['DateOfAbsence'], format='%d/%m/%Y')).dt.dayofyear
        absence_request["DayOfYear"] = (pd.to_datetime(absence_request['DateOfAbsence'], format='%d/%m/%Y')).dayofyear


        #number of employees that are off on the day of requests
        employee_absence_overlap = 0

        #iterate over accepted timeoffs
        for index, absence_data in absence_data_accepted.iterrows():
            #if employee has accepted timeoff in same day as new request, inrement counter
            if absence_request["DayOfYear"] == absence_data['DayOfYear']:
                employee_absence_overlap += 1
        
        actual_capacity =  full_capacity - employee_absence_overlap

        if actual_capacity < min_capacity:
            return False
        else:
            return True
    else:
        return True



def lambda_handler(event, context):
    
    
    dynamodb = boto3.resource('dynamodb')
    
    #absence_data = pd.DataFrame()
    #teams = pd.DataFrame()
    #employees = pd.DataFrame()
    
    ## ---- assigning table paths -----
    path_absence_table = os.environ['ABSENCE_TABLE'] #Absence_Data table DynamoDB
    path_teams_table = os.environ['TEAM_TABLE'] #OU_Table table dynamoDB
    path_employees_table = os.environ['EMPLOYEES_TABLE'] #Employees table dynamoDB
    
    ## ---- loading tables -----
    
    load_absence_table = dynamodb.Table(path_absence_table)
    load_teams_table = dynamodb.Table(path_teams_table)
    load_employees_table = dynamodb.Table(path_employees_table)
    
    
    ## ---- assigning values from tables -----
    absence_table = load_absence_table.scan()
    #print(absence_table)
    absence_data = pd.DataFrame(absence_table['Items'])
    #print(absence_data['Status'])
    absence_data['Employee ID'] = absence_data['Employee ID'].astype(int)
    
    teams_table = load_teams_table.scan()
    teams = pd.DataFrame(teams_table['Items'])
    
    employees_table = load_employees_table.scan()
    #print(employees_table)
    employees = pd.DataFrame(employees_table['Items'])
    #print(employees['OUID'])
    
    
    ##asking for user input
    #absence_data = db.create_absence_request(absence_table)
    #absence_data = db.load_json_table(absence_table, as_df=True)
    #teams = db.load_json_table(teams_table, as_df=True)
    #employees = db.load_json_table(employees_table, as_df=True)
    
    ## sort requests - only "pending"
    requests = absence_data.loc[absence_data['Status'] == '"Pending"']
    #print(requests['Employee ID'])
    #print(employees['EmployeeID'])
    ## sort requests - only "accepted" for comparision in rules
    absence_data_accepted = absence_data.loc[absence_data['Status'] == '"Accepted"']
    
    try:
        ### go through every "pending" requests
        
        for index, request in  requests.iterrows():
            ##get OUID of employee asking timeoff
            requested_from_team_ouid = employees.loc[employees['EmployeeID'] == (request['Employee ID'])]['OUID'].values[0] 
            ##get minimal capacity fact for OU of employee asking timeoff 
            minimal_capacity = teams.loc[teams['OUID'] == requested_from_team_ouid]["MinimalCapacity"].values[0]
           
            ##get all OU members
            team_members_ids = employees.loc[employees['OUID'] == requested_from_team_ouid]["EmployeeID"].values
          
            ##get only absence data from OU from which employee is in
            absence_data_from_team = absence_data_accepted[absence_data_accepted['Employee ID'].isin(team_members_ids)]
            
            ## deciding algorithm (simple if else for now)
            approval = False
            #first rule - checking overlaps in dates
            approval = capacity_rule(minimal_capacity, absence_data_from_team, request, len(team_members_ids))
            if approval:
                print("Request Approved")
                absence_data.loc[absence_data['id'] == request["id"], 'Status'] = '"Accepted"'
            else:
                print("Request Rejected")
                absence_data.loc[absence_data['id'] == request["id"], 'Status'] = '"Rejected"'


            
            #items_list = absence_data.tolist()
            #items_list_response = json.dumps(items_list)
            #print(items_list_response)
            
            #items_list = absence_data.to_json(orient='records')
            #items_list = json.dumps(items_list)
            #print(items_list)
            
            items_list = json.loads(json.dumps(list(absence_data.T.to_dict().values())))
            print(items_list)
            
            item = {
                "id": items_list[0]['id'],
                "Vacation Date": items_list[0]['Vacation Date'],
                "Employee ID":  items_list[0]['Employee ID'],
                "Code Leave Reason": items_list[0]['Code Leave Reason'],
                "Leave Reason": items_list[0]['Leave Reason'],
                "Status": items_list[0]['Status']
            }
            ## save updated value to db
            load_absence_table.put_item(Item=item)
            return "DB TABLE HAS BEEN EDITED !"

    except Exception as e:
        print(e)
        return e
    return "done"
