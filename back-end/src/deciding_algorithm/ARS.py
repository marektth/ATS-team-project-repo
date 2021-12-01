import pandas as pd
import json as json


class ARS(object):

    def __init__(self, absence_data, teams, employees, jobs):
        self.absence_data_path = absence_data
        self.absence_data = self.__load_table(absence_data)
        self.teams = self.__load_table(teams)
        self.employees = self.__load_table(employees)
        self.jobs = self.__load_table(jobs)
            
        self.__rules = {"A": self.rule_overlapping_employees_no,
                "B": self.rule_min_capacity_treshold,
                "C": self.rule_same_job_overlaps,
                "D" : self.rule_min_same_job_treshold
                }
        self.__rules_structs = ['ACBD'] #, 'BCA', 'CBA']

    def __load_table(self, path, as_df=True):
        with open(path) as f:
            json_data = json.load(f)
        if as_df:
            return pd.DataFrame(json_data)
        else:
            return json_data

    def __update_db(self, db):
        if isinstance(db, pd.DataFrame):
            db = db.to_json(orient="records")
            db = json.loads(db)

        with open(self.absence_data_path, 'w') as outfile:
            json.dump(db, outfile, indent=4)

    def __get_requests(self, status = "Pending"):
        return self.absence_data.loc[self.absence_data['Status'] == status]

    def __get_ouid_of_request(self, request):
        return self.employees.loc[self.employees['EmployeeID'] == (request["EmployeeID"])]["OUID"].values[0] 

    def __get_min_capacity_ou(self, request):
        return self.teams.loc[self.teams['OUID'] == self.__get_ouid_of_request(request)]["MinimalCapacity"].values[0]

    def __get_min_same_job_treshold(self, request):
        return self.jobs.loc[self.jobs['id'] == self.__get_employee_info(request, info='EmploymentNumber')]["MinRequirement"].values[0]

    def __get_employee_info(self, request, info = None):
        if info != None:
            return self.employees.loc[self.employees['EmployeeID'] == request['EmployeeID']][info].values[0]
        else:
            return self.employees.loc[self.employees['EmployeeID'] == request['EmployeeID']]

    def __get_ou_employees(self, request, only_id = True):
        if only_id:
            return self.employees.loc[self.employees['OUID'] == self.__get_ouid_of_request(request)]["EmployeeID"].values
        else:
            return self.employees.loc[self.employees['OUID'] == self.__get_ouid_of_request(request)]

    def __get_size_of_ou(self, request):
        return len(self.__get_ou_employees(request))

    def __get_ou_absence_data(self,request, only_accepted = True):
        #future feature - return only recent dates
        if only_accepted:
            accepted_ou_requests = self.__get_requests("Accepted")
            return accepted_ou_requests[accepted_ou_requests['EmployeeID'].isin(self.__get_ou_employees(request))]
        else:
            return self.absence_data[self.absence_data['EmployeeID'].isin(self.__get_ou_employees(request))]

    def __get_ou_same_job_employees(self, request, only_id=False):
        ou_employees = self.__get_ou_employees(request, only_id=False)
        if only_id:
            return ou_employees.loc[ou_employees['EmploymentNumber'] == self.__get_employee_info(request, "EmploymentNumber")]["EmployeeID"].values
        else:
            return ou_employees.loc[ou_employees['EmploymentNumber'] == self.__get_employee_info(request, "EmploymentNumber")]

    def __get_ou_same_job_absence(self, request):
        same_job_employees = self.__get_ou_same_job_employees(request)
        ou_accepted_requests = self.__get_ou_absence_data(request)
        same_job_accepted_requests = ou_accepted_requests[ou_accepted_requests['EmployeeID'].isin(same_job_employees['EmployeeID'].values)]

        return same_job_accepted_requests


    def __convert_to_dayofyear(self, data, column_to_convert, column_to_add, format = '%d/%m/%Y'):
                
        if isinstance(data, pd.DataFrame):
            data[column_to_add] = (pd.to_datetime(data[column_to_convert], format=format)).dt.dayofyear
        else:
            data[column_to_add] = (pd.to_datetime(data[column_to_convert], format=format)).dayofyear
    
        return data




    #################### RULES ####################  

    def rule_overlapping_employees_no(self, request , normalized = True):
        '''
        Check new request if there are overlaping dates with already accepted timeoffs
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
            #if employee has accepted timeoff in same da≤<<y as new request, inrement counter
            if request["DayOfYear"] == absence_data['DayOfYear']:
                employee_absence_overlap_no += 1
        
        if normalized:
            return employee_absence_overlap_no/self.__get_size_of_ou(request)
        else:
            return employee_absence_overlap_no


    def rule_min_capacity_treshold(self, request):
        min_ou_capacity = self.__get_min_capacity_ou(request)
        size_of_ou = self.__get_size_of_ou(request)
        total_missing_employees = self.rule_overlapping_employees_no(request, normalized=False)

        if size_of_ou - total_missing_employees <= min_ou_capacity:
            return 0
        else:
            return 1


    def rule_same_job_overlaps(self,request, normalized=True):
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
            #if employee has accepted timeoff in same day as new request, inrement counter
            if request["DayOfYear"] == absence_data['DayOfYear']:
                employee_absence_overlap_no += 1
        
        if normalized:
            return employee_absence_overlap_no/self.__get_size_of_ou(request)
        else:
            return employee_absence_overlap_no



    def rule_min_same_job_treshold(self, request):
        min_same_job_tresh = self.__get_min_same_job_treshold(request)
        same_job_employee_no = len(self.__get_ou_same_job_employees(request, only_id=True))
        total_missing_employees = self.rule_same_job_overlaps(request, normalized=False)

        if same_job_employee_no - total_missing_employees <= min_same_job_tresh:
            return 0
        else:
            return 1



    def rating_function(self):

        pending_requests = self.__get_requests(status = "Pending")

        for request_idx, pending_request in pending_requests.iterrows():
            request_rating = dict()
            for rule in self.__rules_structs[0]:
                rule_to_call = self.__rules[rule]
                request_rating[rule] = rule_to_call(pending_request)
            
            self.absence_data.at[request_idx, 'Rating'] = dict(sorted(request_rating.items()))
        
        self.__update_db(self.absence_data)


    # def __comapre_requests(self):
    #     '''
    #         to implement,
    #         severity could be modified based on overlapping, tresholds, ...
    #     '''
        
    #     pass
    
    # def __set_request_status(self):
    #     '''
    #         to implement,
    #         change status "Pending" to "Accepted"/"Declined" based on severity, possibly use fuzzy
    #     '''
    #     pass




if __name__ == "__main__":
    path_absence_table = "back-end/src/data/jsons/absence_data.json"
    path_teams_table = "back-end/src/data/jsons/teams_table.json"
    path_employees_table = "back-end/src/data/jsons/employees_table.json"
    path_jobs_table = "back-end/src/data/jsons/jobs_table.json"

    ars = ARS(path_absence_table, path_teams_table, path_employees_table, path_jobs_table)
    ars.rating_function()
