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
            Loads file.json to pandas.Dataframe or JSON object
            :param path: str - path to JSON file
            :param as_df: bool - if return pandas.DataFrame or JSON object
            :return: returns pandas.DataFrame or JSON object loaded from file
            :rtype: pandas.DataFrame or JSON object
        '''
        if as_df:
            return pd.read_json(path)
        else:
            with open(path) as f:
                json_data = json.load(f)
            return json_data

    def update_db(self, db, data_path):
        '''
            Updates file.json specified in data_path
            :param db: pandas.DataFrame or JSON object
            :param data_path: str - path to JSON file
            :return: returns nothing
        '''
        if isinstance(db, pd.DataFrame):
            db = db.to_json(orient="records")
            db = json.loads(db)

        with open(data_path, 'w') as outfile:
            json.dump(db, outfile, indent=4)

    def update_item(self, value, row_idx, column, table):
        '''
            Updates row at column in table with given value
            :param value: any - value to update in pandas.DataFrame
            :param row_idx: int - index of row to update cell
            :param column: str - name of column to update cell
            :param table: pandas.DataFrame - table where to update cell
            :return: returns nothing
        '''
        table.at[row_idx, column] = value


    def __rules_preprocessing(self, rules):
        '''
            Drop unused rules for specific customer
            To activate rule attribute 'testByThisRule' must be set to True
            :param rules: pandas.DataFrame - table with rules
            :return: active rules to test with
            :rtype: pandas.DataFrame
        '''
        return rules[rules['testByThisRule'] == True]

    def get_requests(self, status = "Pending"):
        '''
            Returns all absence data with given status
            :param status: string - "Pending", "Rejected", "Accepted", "Cancelled"
            :return: returns requests marked with specified status
            :rtype: pandas.DataFrame
        '''
        return self.absence_data.loc[self.absence_data['Status'] == status]

    def get_ouid_of_request(self, request):
        '''
            Returns ID of OU of given request
            :param request: pandas.Series
            :return: returns organization unit ID
            :rtype: int
        '''
        return self.employees.loc[self.employees['EmployeeID'] == (request["EmployeeID"])]["OUID"].values[0] 

    def get_min_capacity_ou(self, request):
        '''
            Returns required minimal capacity of OU of given request
            :param request: pandas.Series
            :return: returns teams table attribute "MinimalCapacity" 
            :rtype: int
        '''
        return self.teams.loc[self.teams['OUID'] == self.get_ouid_of_request(request)]["MinimalCapacity"].values[0]

    def get_min_same_job_threshold(self, request):
        '''
            Returns required minimum of present people with same job as request job
            :param request: pandas.Series
            :return: returns jobs table attribute "MinRequirement" 
            :rtype: int
        '''
        return self.jobs.loc[self.jobs['id'] == self.get_employee_info(request, info='EmploymentNumber')]["MinRequirement"].values[0]

    def get_employee_info(self, request, info = None):
        '''
            Returns info about employee of given request
            :param request: pandas.Series
            :param info: str - any employee table attribute (default:None)
            :return: default returns whole record of employee of given request
            :rtype: int/str/(default:pandas.DataFrame)
        '''
        if info != None:
            return self.employees.loc[self.employees['EmployeeID'] == request['EmployeeID']][info].values[0]
        else:
            return self.employees.loc[self.employees['EmployeeID'] == request['EmployeeID']]

    def get_ou_employees(self, request, only_id = True):
        '''
            Returns all employees in OU of given request
            optional: returns only employees ID in OU of given request
            :param request: pandas.Series
            :param only_id: bool - if return only id of request (default:True)
            :return: default returns only id of employees in same OU as request
            :rtype: pandas.DataFrame/(default:list of int(s))
        '''
        if only_id:
            return self.employees.loc[self.employees['OUID'] == self.get_ouid_of_request(request)]["EmployeeID"].values
        else:
            return self.employees.loc[self.employees['OUID'] == self.get_ouid_of_request(request)]

    def get_size_of_ou(self, request):
        '''
            Returns size of OU of given request
            :param request: pandas.Series
            :return: returns size of OU of given request
            :rtype: int
        '''
        return len(self.get_ou_employees(request))

    def get_ou_absence_data(self,request, status_of_absence = "Accepted"):
        '''
            Returns OU absence data in which request employee is in 
            optional: if "status_of_absence" is set to "Accepted"/"Rejected"/"Pending", method returns only OU absence data with specified status
                      if "status_of_absence" is set to "All" returns all OU absence data
            :param request: pandas.Series
            :param status_of_absence: string - "Pending", "Rejected", "Accepted", "Cancelled", "All"
            :return: returns requests marked with specified status
            :rtype: pandas.DataFrame
        '''
        if status_of_absence in ("Accepted", "Rejected", "Pending", "Cancelled"):
            ou_requests_per_status = self.get_requests(status_of_absence)
            return ou_requests_per_status[ou_requests_per_status['EmployeeID'].isin(self.get_ou_employees(request))]
        elif status_of_absence == "All":
            return self.absence_data[self.absence_data['EmployeeID'].isin(self.get_ou_employees(request))]

    def get_ou_same_job_employees(self, request, only_id=False):
        '''
            Returns employees with same job as request job
            optional: if parameter "only_id" is set to True, method returns only ids of employees of same job in same OU
                      if parameter "only_id" is set to False returns whole records of employees of same job in same OU
            :param request: pandas.Series
            :param only_id: bool - True/(defaul:False)
            :return: returns employees ids in list or whole records of employees
            :rtype: list of int(s)/(default:pandas.DataFrame)
        '''
        ou_employees = self.get_ou_employees(request, only_id=False)
        if only_id:
            return ou_employees.loc[ou_employees['EmploymentNumber'] == self.get_employee_info(request, "EmploymentNumber")]["EmployeeID"].values
        else:
            return ou_employees.loc[ou_employees['EmploymentNumber'] == self.get_employee_info(request, "EmploymentNumber")]

    def get_ou_same_job_absence(self, request):
        '''
            Returns absence data of OU only of same job as request job
            :param request: pandas.Series
            :return: returns absence data of OU only of same job as request job
            :rtype: pandas.DataFrame
        '''
        same_job_employees = self.get_ou_same_job_employees(request)
        ou_accepted_requests = self.get_ou_absence_data(request)
        same_job_accepted_requests = ou_accepted_requests[ou_accepted_requests['EmployeeID'].isin(same_job_employees['EmployeeID'].values)]

        return same_job_accepted_requests

    def format_absence_dates(self, data, columns=['AbsenceFrom', 'AbsenceTo'], format = '%d/%m/%Y'):
        '''
            Returns formated specified columns using format in data
            :param data: pandas.Series or pandas.DataFrame
            :param columns: list - two columns with string dates values to format (default:['AbsenceFrom', 'AbsenceTo'])
            :param format: str - format type (default:'%d/%m/%Y') 
            :return: returns data with formatted dates (using pandas.to_datetime()) in two specified columns
            :rtype: pandas.Series or pandas.DataFrame
        '''
        data[columns[0]] = pd.to_datetime(data[columns[0]], format=format)
        data[columns[1]] = pd.to_datetime(data[columns[1]], format=format)

        return data


    def get_absence_type_priority(self, request):
        '''
            Returns absence type priority of specified request
            :param request: pandas.Series
            :return: returns absence type priority of specified request
            :rtype: int
        '''
        return self.absence_type.loc[self.absence_type['AbsenceAcronym'] == request['AbsenceTypeCode']]["Priority"].values[0]

    
    def get_request_leave_hours(self, request, working_hours=8):
        '''
            Returns total leave hours of requested absence
            Business days - (Mon, Tue, Wed, Thu, Fri) starting week on Monday
            Request AbsenceFrom and AbsenceTo in format '%d/%m/%Y'
            :param request: pandas.Series
            :param working_hours: int - usual working hours (default:8)
            :return: returns number of requested business hours absence
            :rtype: int
            ** future feature ** - check if year has 356 or 366 days
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
            Returns True if request has enough leave balance left
            :param request: pandas.Series
            :return: returns bool, if enough balance True else False
            :rtype: bool
        '''
        return self.get_employee_info(request, info = "LeaveBalance") - self.get_request_leave_hours(request) >= 0
    
    def set_ou_rating_duration(self, ouid, start_time):
        '''
            Sets duration of rating and changing statuses of pending ou requests
            Sets LastChangeMS timestamp
            :param ouid: int - id of organization unit
            :param start_time: float - time in seconds since the Epoch 
            :return: nothing
        '''
        end_time = time.time()
        duration = (end_time - start_time)*1000
        self.teams.loc[self.teams['OUID'] == ouid, 'LastChangeMS'] = end_time
        self.teams.loc[self.teams['OUID'] == ouid, 'RatingDurationMS'] = duration
    
    def get_rules_by_keys(self):
        '''
            Returns rules keys and corresponding functions to call
            :return: active rules keys and corresponding functions names to call
            :rtype: list of dicts
        '''
        return (self.rules[["key","function"]]).to_dict(orient="records") 

    def get_rules_with_order(self):
        '''
            Returns tuple (rules keys in priority order, sort order booleans)
            :return: tuple with sorted keys in priority order
            :rtype: tuple of integers
        '''
        keys_with_priorities = (self.rules[["key","priority","sortAscending"]]).sort_values(by="priority")
        return (keys_with_priorities["key"].values).tolist(), (keys_with_priorities["sortAscending"].values).tolist()     
    
    def get_rule_threshold_by_key(self, rule_key):
        '''
            Returns threshold for specified rule by key
            :param rule_key: str - key of rule
            :return: threshold for specified rule by key
            :rtype: int
        '''
        return self.rules.loc[self.rules['key'] == rule_key]["threshold"].values[0]

    def get_rule_status_failed_resolution(self, rule_key):
        '''
            Returns resolution of rule for specified failed rule by key
            :param rule_key: str - key of rule
            :return: resolution why rule failed
            :rtype: str
        '''
        return self.rules.loc[self.rules['key'] == rule_key]["resolutionFailed"].values[0]

    def get_overlapping_days(self, range1, range2):
        '''
            Returns set overlapping days between ranges
            usage:  >>> overlapping_days = get_overlapping_days(*range1) & get_overlapping_days(*range2)
            :param range1: list - list with two elements [Timestamp, Timestamp]
            :param range2: list - list with two elements [Timestamp, Timestamp]
            :return: every overlapping days
            :rtype: set
        '''
        delta = range2 - range1
        return set([range1 + timedelta(days=i) for i in range(delta.days + 1)])
            