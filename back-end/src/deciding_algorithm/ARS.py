import pandas as pd
import json as json


class ARS(object):

    def __init__(self, absence_data, teams, employees, jobs, absence_type):
        '''
            - initialize all tables from DB
            - initialze rules to use in rating, rules order and rules tresholds
        '''
        self.absence_data_path = absence_data
        self.absence_data = self.__load_table(absence_data)
        self.teams = self.__load_table(teams)
        self.employees = self.__load_table(employees)
        self.jobs = self.__load_table(jobs)
        self.absence_type = self.__load_table(absence_type)
            
        self.__rules = {
                        "A": self.rule_min_capacity_treshold,
                        "B" : self.rule_min_same_job_treshold,
                        "C" : self.rule_set_absence_type_priority
                        }

        self.__rules_structs = ['C','B','A']
        self.__rules_df_sort = [True,False,False]
        self.__rules_tresholds = {
            "A" : 1,
            "B" : 1,
        }

    def __load_table(self, path, as_df=True):
        '''
        here implement AWS table loading functions
        '''
        with open(path) as f:
            json_data = json.load(f)
        if as_df:
            return pd.DataFrame(json_data)
        else:
            return json_data

    def __update_db(self, db):
        '''
        update db at the end of algorithm
        here implement AWS table updating functions
        '''
        if isinstance(db, pd.DataFrame):
            db = db.to_json(orient="records")
            db = json.loads(db)

        with open(self.absence_data_path, 'w') as outfile:
            json.dump(db, outfile, indent=4)

    def __update_item(self, value, row_idx, column, table):
        '''
            updates row at column in table with given value
        '''
        table.at[row_idx, column] = value

    def __get_requests(self, status = "Pending"):
        '''
            returns all absence data with given status
        '''
        return self.absence_data.loc[self.absence_data['Status'] == status]

    def __get_ouid_of_request(self, request):
        '''
            returns ID of OU of given request
        '''
        return self.employees.loc[self.employees['EmployeeID'] == (request["EmployeeID"])]["OUID"].values[0] 

    def __get_min_capacity_ou(self, request):
        '''
            returns required minimal capacity of OU of given request
        '''
        return self.teams.loc[self.teams['OUID'] == self.__get_ouid_of_request(request)]["MinimalCapacity"].values[0]

    def __get_min_same_job_treshold(self, request):
        '''
            returns required minimum of present people with same job as request job
        '''
        return self.jobs.loc[self.jobs['id'] == self.__get_employee_info(request, info='EmploymentNumber')]["MinRequirement"].values[0]

    def __get_employee_info(self, request, info = None):
        '''
            returns info of employee of given request
            optional: return only specified information if parameter "info" given 
                otherwise returns whole employee record
        '''
        if info != None:
            return self.employees.loc[self.employees['EmployeeID'] == request['EmployeeID']][info].values[0]
        else:
            return self.employees.loc[self.employees['EmployeeID'] == request['EmployeeID']]

    def __get_ou_employees(self, request, only_id = True):
        '''
            returns all employees in OU of given request
            optional: returns only employees ID in OU of given request
                otherwise returns whole employees records
        '''
        if only_id:
            return self.employees.loc[self.employees['OUID'] == self.__get_ouid_of_request(request)]["EmployeeID"].values
        else:
            return self.employees.loc[self.employees['OUID'] == self.__get_ouid_of_request(request)]

    def __get_size_of_ou(self, request):
        '''
            returns size of OU of given request
        '''
        return len(self.__get_ou_employees(request))

    def __get_ou_absence_data(self,request, status_of_absence = "Accepted"):
        '''
            returns OU absence data in which request employee is in
            **future feature - returns only recent dates**
            optional: if "status_of_absence" is set ("Accepted", "Reqected", "Pending"), returns only specified absence_data
                otherwise returns all
        '''
        if status_of_absence in ("Accepted", "Reqected", "Pending"):
            ou_requests_per_status = self.__get_requests(status_of_absence)
            return ou_requests_per_status[ou_requests_per_status['EmployeeID'].isin(self.__get_ou_employees(request))]
        if status_of_absence == "All":
            return self.absence_data[self.absence_data['EmployeeID'].isin(self.__get_ou_employees(request))]

    def __get_ou_same_job_employees(self, request, only_id=False):
        '''
            returns employees with same job as request job
            optional: if parameter "only_id" is set, returns only id of employees of same job in same OU
                otherwise returns whole records
        '''
        ou_employees = self.__get_ou_employees(request, only_id=False)
        if only_id:
            return ou_employees.loc[ou_employees['EmploymentNumber'] == self.__get_employee_info(request, "EmploymentNumber")]["EmployeeID"].values
        else:
            return ou_employees.loc[ou_employees['EmploymentNumber'] == self.__get_employee_info(request, "EmploymentNumber")]

    def __get_ou_same_job_absence(self, request):
        '''
            returns absence data of OU only of same job as request job
        '''
        same_job_employees = self.__get_ou_same_job_employees(request)
        ou_accepted_requests = self.__get_ou_absence_data(request)
        same_job_accepted_requests = ou_accepted_requests[ou_accepted_requests['EmployeeID'].isin(same_job_employees['EmployeeID'].values)]

        return same_job_accepted_requests


    def __convert_to_dayofyear(self, data, column_to_convert, column_to_add, format = '%d/%m/%Y'):
        '''
            converts date in speficied format to day in year (01/01/2021 -> 1)
            adds column with specified name in which converted dates are stored in
            returns dataframe with new column
        '''
                
        if isinstance(data, pd.DataFrame):
            data[column_to_add] = (pd.to_datetime(data[column_to_convert], format=format)).dt.dayofyear
        else:
            data[column_to_add] = (pd.to_datetime(data[column_to_convert], format=format)).dayofyear
    
        return data

    def __get_absence_type_priority(self, request):
        '''
            returns absence type priority of specified request
        '''
        return self.absence_type.loc[self.absence_type['AbsenceAcronym'] == request['AbsenceTypeCode']]["Priority"].values[0]





    #################### RULES ####################  

    def rule_overlapping_employees_no(self, request , normalized = True):
        '''
            returns number of overlapping employees with already accepted timeoffs with dates of given requests 
            optional: normalized, if set true, returns percentage of absent employees
                otherwise returns count of absent employees
        '''

        if request.empty:
            return None

        ou_absence_data = self.__get_ou_absence_data(request)

        if(ou_absence_data.empty):
            return 0

        #convert to day of year
        ou_absence_data = self.__convert_to_dayofyear(data=ou_absence_data, column_to_convert='DateOfAbsence', column_to_add='DayOfYear')
        request = self.__convert_to_dayofyear(request, column_to_convert='DateOfAbsence', column_to_add='DayOfYear')

        #number of employees that are off on the day of requests
        employee_absence_overlap_no = 0

        #iterate over accepted timeoffs
        for _, absence_data in ou_absence_data.iterrows():
            #if employee has accepted timeoff in same day as new request, increment counter
            if request["DayOfYear"] == absence_data['DayOfYear']:
                employee_absence_overlap_no += 1
        
        if normalized:
            return employee_absence_overlap_no/self.__get_size_of_ou(request)
        else:
            return employee_absence_overlap_no


    def rule_min_capacity_treshold(self, request):
        '''
            returns if minimal OU capacity treshhold is exceeded
        '''
        min_ou_capacity = self.__get_min_capacity_ou(request)
        size_of_ou = self.__get_size_of_ou(request)
        total_missing_employees = self.rule_overlapping_employees_no(request, normalized=False)

        if size_of_ou - total_missing_employees <= min_ou_capacity:
            return 1
        else:
            return 0


    def rule_same_job_overlaps(self,request, normalized=True):
        '''
            returns number of overlapping employees with already accepted timeoffs with dates of given requests
            where same job employees are compared
            optional: normalized, if set true, returns percentage of absent employees with same job
                otherwise returns count of absent employees with same job
        '''
        if request.empty:
            return None

        same_job_absence_data = self.__get_ou_same_job_absence(request)

        if(same_job_absence_data.empty):
            return 0

        #convert to day of year
        same_job_absence_data = self.__convert_to_dayofyear(data=same_job_absence_data, column_to_convert='DateOfAbsence', column_to_add='DayOfYear')
        request = self.__convert_to_dayofyear(request, column_to_convert='DateOfAbsence', column_to_add='DayOfYear')

        #number of employees that are off on the day of requests
        employee_absence_overlap_no = 0

        #iterate over accepted timeoffs
        for _, absence_data in same_job_absence_data.iterrows():
            #if employee has accepted timeoff in same day as new request, increment counter
            if request["DayOfYear"] == absence_data['DayOfYear']:
                employee_absence_overlap_no += 1
        
        if normalized:
            return employee_absence_overlap_no/self.__get_size_of_ou(request)
        else:
            return employee_absence_overlap_no



    def rule_min_same_job_treshold(self, request):
        '''
            returns if absent same job employees treshhold is exceeded
        '''
        min_same_job_tresh = self.__get_min_same_job_treshold(request)
        same_job_employee_no = len(self.__get_ou_same_job_employees(request, only_id=True))
        total_missing_employees = self.rule_same_job_overlaps(request, normalized=False)

        if same_job_employee_no - total_missing_employees <= min_same_job_tresh:
            return 1
        else:
            return 0

    def rule_set_absence_type_priority(self, request):
        '''
            returns absent type priority of given request
        '''
        return self.__get_absence_type_priority(request)
        

    def rating_function(self):
        '''
            rate all pending requests based on rules specified in "self.__rules_structs"
            saves ratings in dataframe
        '''
        pending_requests = self.__get_requests(status = "Pending")

        for request_idx, pending_request in pending_requests.iterrows():
            request_rating = dict()
            for rule in self.__rules_structs:
                rule_to_call = self.__rules[rule]
                request_rating[rule] = rule_to_call(pending_request)
            
            #place to save item
            self.__update_item(dict(sorted(request_rating.items())), request_idx, "Rating", self.absence_data)
        
        #for testing purposes only
        #do not use in AWS !!
        #self.__update_db(self.absence_data)


    def set_top_priority_request_status(self):
        '''
            to implement
        '''

        pending_requests = self.__get_requests(status = "Pending")
        severities_df = pd.DataFrame((pending_requests["Rating"]).apply(pd.Series), index=pending_requests.index)

        severities_df.sort_values(by=self.__rules_structs, ascending=self.__rules_df_sort, inplace=True)

        top_request = severities_df.iloc[0]
        request_decision = "Accepted"
        for rule_rank in self.__rules_structs:
            #out of treshold - Reject
            #future feature - maybe do helper microrules to really decide if rejected
            if rule_rank in self.__rules_tresholds and top_request[rule_rank] >= self.__rules_tresholds[rule_rank]:
                request_decision = "Rejected"
                break

        self.__update_item(request_decision, top_request.name, "Status", self.absence_data)

    def absence_request_handle(self):
        while len(self.__get_requests(status = "Pending")):
            self.rating_function()
            self.set_top_priority_request_status()

        print(self.absence_data)






if __name__ == "__main__":
    path_absence_table = "back-end/src/data/jsons/absence_data.json"
    path_teams_table = "back-end/src/data/jsons/teams_table.json"
    path_employees_table = "back-end/src/data/jsons/employees_table.json"
    path_jobs_table = "back-end/src/data/jsons/jobs_table.json"
    path_absence_type_table = "back-end/src/data/jsons/absence_type.json"

    ars = ARS(path_absence_table, path_teams_table, path_employees_table, path_jobs_table, path_absence_type_table)
    ars.absence_request_handle()
