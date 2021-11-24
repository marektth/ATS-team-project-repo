from numpy import empty
import db_get_data as db 
import pandas as pd
import datetime    



def capacity_rule(min_capacity, absence_data_accepted, absence_request, full_capacity):
    '''
        Check new request if there are overlaping dates with already accepted timeoffs
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
            #return serverity value
            return False
        else:
            return True
    else:
        return True


def main():

    ## ---- loading tables -----
    path_absence_table = "back-end/src/data/jsons/absence_data.json"
    path_teams_table = "back-end/src/data/jsons/teams_table.json"
    path_employees_table = "back-end/src/data/jsons/employees_table.json"

    ##asking for user input
    absence_data = db.create_absence_request(path_absence_table)


    absence_data = db.load_json_table(path_absence_table, as_df=True)
    teams = db.load_json_table(path_teams_table, as_df=True)
    employees = db.load_json_table(path_employees_table, as_df=True)

    ## sort requests - only "pending"
    requests = absence_data.loc[absence_data['Status'] == "Pending"]

    ## sort requests - only "accepted" for comparision in rules
    absence_data_accepted = absence_data.loc[absence_data['Status'] == "Accepted"]

    try:
        ### go through every "pending" requests
        for index, request in  requests.iterrows():
            ##get OUID of employee asking timeoff
            requested_from_team_ouid = employees.loc[employees['EmployeeID'] == (request["EmployeeID"])]["OUID"].values[0] 

            ##get minimal capacity fact for OU of employee asking timeoff 
            minimal_capacity = teams.loc[teams['OUID'] == requested_from_team_ouid]["MinimalCapacity"].values[0]

            ##get all OU members
            team_members_ids = employees.loc[employees['OUID'] == requested_from_team_ouid]["EmployeeID"].values

            ##get only absence data from OU from which employee is in
            absence_data_from_team = absence_data_accepted[absence_data_accepted['EmployeeID'].isin(team_members_ids)]
            
            ## deciding algorithm (simple if else for now)
            approval = False
            #first rule - checking overlaps in dates
            approval = capacity_rule(minimal_capacity, absence_data_from_team, request, len(team_members_ids))
            if approval:
                print("Request Approved")
                absence_data.loc[absence_data['id'] == request["id"], 'Status'] = "Accepted"
            else:
                print("Request Rejected")
                absence_data.loc[absence_data['id'] == request["id"], 'Status'] = "Rejected"

            ## save updated value to db
            db.update_json_table(path_absence_table, absence_data)

    except Exception as e: 
        print(e)

if __name__ == "__main__":
    main()