import pandas as pd
import numpy as np
import json
import time
from datetime import timedelta, datetime

class DBHandler():
    def __init__(self, absence_data, teams, employees, jobs, absence_type, rules):
        '''
            - initialize all tables from DB
            - initialze rules to use in rating, rules order and rules thresholds
        '''
        self.absence_data_path = absence_data
        self.teams_data_path = teams
        self.absence_data = self.__load_table(absence_data)
        self.teams = self.__load_table(teams)
        self.employees = self.__load_table(employees)
        self.jobs = self.__load_table(jobs)
        self.absence_type = self.__load_table(absence_type)
        self.rules = self.__load_table(rules)

        self.rules = self.__rules_preprocessing(self.rules)

    def __load_table(self, path, as_df=True):
        '''
        here implement AWS table loading functions
        '''
        if as_df:
            return pd.read_json(path)
        else:
            with open(path) as f:
                json_data = json.load(f)
            return json_data

    def update_db(self, db, data_path):
        '''
        update db at the end of algorithm
        here implement AWS table updating functions
        '''
        if isinstance(db, pd.DataFrame):
            db = db.to_json(orient="records")
            db = json.loads(db)

        with open(data_path, 'w') as outfile:
            json.dump(db, outfile, indent=4)

    def update_item(self, value, row_idx, column, table):
        '''
            updates row at column in table with given value
        '''
        table.at[row_idx, column] = value


    def __rules_preprocessing(self, rules):
        '''
            drop unused rules for specific customer
        '''
        return rules[rules['testByThisRule'] == True]

    def get_requests(self, status = "Pending"):
        '''
            returns all absence data with given status
        '''
        return self.absence_data.loc[self.absence_data['Status'] == status]

    def get_request_by_id(self, request_id):
        '''
            returns request record by its id
        '''
        absence_request = self.absence_data.loc[self.absence_data["id"] == request_id]
        return absence_request.iloc[0]

    def get_ouid_of_request(self, request):
        '''
            returns ID of OU of given request
        '''
        return self.employees.loc[self.employees['EmployeeID'] == (request["EmployeeID"])]["OUID"].values[0] 

    def get_min_capacity_ou(self, request):
        '''
            returns required minimal capacity of OU of given request
        '''
        return self.teams.loc[self.teams['OUID'] == self.get_ouid_of_request(request)]["MinimalCapacity"].values[0]

    def get_min_same_job_threshold(self, request):
        '''
            returns required minimum of present people with same job as request job
        '''
        return self.jobs.loc[self.jobs['id'] == self.get_employee_info(request, info='EmploymentNumber')]["MinRequirement"].values[0]

    def get_employee_info(self, request, info = None):
        '''
            returns info of employee of given request
            optional: return only specified information if parameter "info" given 
                otherwise returns whole employee record
        '''
        if info != None:
            return self.employees.loc[self.employees['EmployeeID'] == request['EmployeeID']][info].values[0]
        else:
            return self.employees.loc[self.employees['EmployeeID'] == request['EmployeeID']]

    def get_ou_employees(self, request, only_id = True):
        '''
            returns all employees in OU of given request
            optional: returns only employees ID in OU of given request
                otherwise returns whole employees records
        '''
        if only_id:
            return self.employees.loc[self.employees['OUID'] == self.get_ouid_of_request(request)]["EmployeeID"].values
        else:
            return self.employees.loc[self.employees['OUID'] == self.get_ouid_of_request(request)]

    def get_size_of_ou(self, request):
        '''
            returns size of OU of given request
        '''
        return len(self.get_ou_employees(request))

    def get_ou_absence_data(self,request, status_of_absence = "Accepted"):
        '''
            returns OU absence data in which request employee is in
            **future feature - returns only recent dates**
            optional: if "status_of_absence" is set ("Accepted", "Rejected", "Pending"), returns only specified absence_data
                otherwise returns all
        '''
        if status_of_absence in ("Accepted", "Rejected", "Pending", "Cancelled"):
            ou_requests_per_status = self.get_requests(status_of_absence)
            return ou_requests_per_status[ou_requests_per_status['EmployeeID'].isin(self.get_ou_employees(request))]
        elif status_of_absence == "All":
            return self.absence_data[self.absence_data['EmployeeID'].isin(self.get_ou_employees(request))]

    def get_ou_same_job_employees(self, request, only_id=False):
        '''
            returns employees with same job as request job
            optional: if parameter "only_id" is set, returns only id of employees of same job in same OU
                otherwise returns whole records
        '''
        ou_employees = self.get_ou_employees(request, only_id=False)
        if only_id:
            return ou_employees.loc[ou_employees['EmploymentNumber'] == self.get_employee_info(request, "EmploymentNumber")]["EmployeeID"].values
        else:
            return ou_employees.loc[ou_employees['EmploymentNumber'] == self.get_employee_info(request, "EmploymentNumber")]

    def get_ou_same_job_absence(self, request):
        '''
            returns absence data of OU only of same job as request job
        '''
        same_job_employees = self.get_ou_same_job_employees(request)
        ou_accepted_requests = self.get_ou_absence_data(request)
        same_job_accepted_requests = ou_accepted_requests[ou_accepted_requests['EmployeeID'].isin(same_job_employees['EmployeeID'].values)]

        return same_job_accepted_requests

    def format_absence_dates(self, data, columns=['AbsenceFrom', 'AbsenceTo'], format = '%d/%m/%Y'):
        '''
            returns formated specified columns by format in data
            param columns must be list of 2 columns
        '''

        data[columns[0]] = pd.to_datetime(data[columns[0]], format=format)
        data[columns[1]] = pd.to_datetime(data[columns[1]], format=format)

        return data


    def get_absence_type_priority(self, request):
        '''
            returns absence type priority of specified request
        '''
        return self.absence_type.loc[self.absence_type['AbsenceAcronym'] == request['AbsenceTypeCode']]["Priority"].values[0]

    
    def get_request_leave_hours(self, request, working_hours=8):
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

    def check_enough_leave_balance(self, request):
        '''
            returns True if request has enough leave balance left
        '''
        return self.get_employee_info(request, info = "LeaveBalance") - self.get_request_leave_hours(request) >= 0
    
    def set_ou_rating_duration(self, ouid, start_time):
        '''
            set duration of rating and changing statuses of pending ou requests
        '''
        end_time = time.time()
        duration = (end_time - start_time)*1000
        self.teams.loc[self.teams['OUID'] == ouid, 'LastChangeMS'] = end_time
        self.teams.loc[self.teams['OUID'] == ouid, 'RatingDurationMS'] = duration
    
    def get_rules_by_keys(self):
        '''
            returns rules keys and corresponding functios to call as list of DICTs
        '''
        return (self.rules[["key","function"]]).to_dict(orient="records") 

    def get_rules_with_order(self):
        '''
            returns tuple (rules keys in priority order, sort order booleans)
            
        '''
        keys_with_priorities = (self.rules[["key","priority","sortAscending"]]).sort_values(by="priority")
        return (keys_with_priorities["key"].values).tolist(), (keys_with_priorities["sortAscending"].values).tolist()     
    
    def get_rule_threshold_by_key(self, rule_key):
        '''
            returns threshold for specified rule by key
        '''
        return self.rules.loc[self.rules['key'] == rule_key]["threshold"].values[0]

    def get_rule_status_failed_resolution(self, rule_key):
        '''
            returns resolution of rule for specified failed rule by key
        '''
        return self.rules.loc[self.rules['key'] == rule_key]["resolutionFailed"].values[0]

    def get_overlapping_days(self, range1, range2):
        '''
            returns set overlapping days between ranges
            usage:  >>> overlapping_days = get_overlapping_days(*range1) & get_overlapping_days(*range2)
        '''
        delta = range2 - range1
        return set([range1 + timedelta(days=i) for i in range(delta.days + 1)])
            