#from src.Absence_rating_system.Data_handler import DBHandler
from Data_handler import DBHandler
import pandas as pd

class ARS(object):

    def __init__(self, absence_data, teams, employees, jobs, absence_type):

        self.db = DBHandler(absence_data, teams, employees, jobs, absence_type)
        self.__rules = {
                "A": self.rule_min_capacity_treshold,
                "B" : self.rule_min_same_job_treshold,
                "C" : self.rule_set_absence_type_priority,
                "D" : self.rule_leave_balance

                }

        self.__rules_structs = ['C','B','A','D']
        self.__rules_df_sort = [True,False,False,False]
        self.__rules_tresholds = {
            "A" : 1,
            "B" : 1,
            "D" : 0,
        }

    def rule_overlapping_employees_no(self, request , normalized = True):
        '''
            returns number of overlapping employees with already accepted timeoffs with dates of given requests 
            optional: normalized, if set true, returns percentage of absent employees
                otherwise returns count of absent employees
        '''

        if request.empty:
            return None

        ou_absence_data = self.db.get_ou_absence_data(request)

        if(ou_absence_data.empty):
            return 0

        #convert to day of year
        ou_absence_data = self.db.convert_to_dayofyear(data=ou_absence_data, column_to_convert='DateOfAbsence', column_to_add='DayOfYear')
        request = self.db.convert_to_dayofyear(request, column_to_convert='DateOfAbsence', column_to_add='DayOfYear')

        #number of employees that are off on the day of requests
        employee_absence_overlap_no = 0

        #iterate over accepted timeoffs
        for _, absence_data in ou_absence_data.iterrows():
            #if employee has accepted timeoff in same day as new request, increment counter
            if request["DayOfYear"] == absence_data['DayOfYear']:
                employee_absence_overlap_no += 1
        
        if normalized:
            return employee_absence_overlap_no/self.db.get_size_of_ou(request)
        else:
            return employee_absence_overlap_no


    def rule_min_capacity_treshold(self, request):
        '''
            returns if minimal OU capacity treshhold is exceeded
        '''
        min_ou_capacity = self.db.get_min_capacity_ou(request)
        size_of_ou = self.db.get_size_of_ou(request)
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

        same_job_absence_data = self.db.get_ou_same_job_absence(request)

        if(same_job_absence_data.empty):
            return 0

        #convert to day of year
        same_job_absence_data = self.db.convert_to_dayofyear(data=same_job_absence_data, column_to_convert='DateOfAbsence', column_to_add='DayOfYear')
        request = self.db.convert_to_dayofyear(request, column_to_convert='DateOfAbsence', column_to_add='DayOfYear')

        #number of employees that are off on the day of requests
        employee_absence_overlap_no = 0

        #iterate over accepted timeoffs
        for _, absence_data in same_job_absence_data.iterrows():
            #if employee has accepted timeoff in same day as new request, increment counter
            if request["DayOfYear"] == absence_data['DayOfYear']:
                employee_absence_overlap_no += 1
        
        if normalized:
            return employee_absence_overlap_no/self.db.get_size_of_ou(request)
        else:
            return employee_absence_overlap_no



    def rule_min_same_job_treshold(self, request):
        '''
            returns if absent same job employees treshhold is exceeded
        '''
        min_same_job_tresh = self.db.get_min_same_job_treshold(request)
        same_job_employee_no = len(self.db.get_ou_same_job_employees(request, only_id=True))
        total_missing_employees = self.rule_same_job_overlaps(request, normalized=False)
        if same_job_employee_no - total_missing_employees <= min_same_job_tresh:
            return 1
        else:
            return 0

    def rule_set_absence_type_priority(self, request):
        '''
            returns absent type priority of given request
        '''
        return self.db.get_absence_type_priority(request) 


    def rule_leave_balance(self, request):
        '''
            returns absent type priority of given request
        '''
        if self.db.check_enough_leave_balance(request) and request["AbsenceTypeCode"] == "TIM" :
            return self.db.get_employee_info(request, info = "LeaveBalance")
        elif not (self.db.check_enough_leave_balance(request)) and request["AbsenceTypeCode"] == "TIM":
            return 0
        else:
            return 1


        
        

    def rating_function(self):
        '''
            rate all pending requests based on rules specified in "self.__rules_structs"
            saves ratings in dataframe
        '''
        pending_requests = self.db.get_requests(status = "Pending")

        for request_idx, pending_request in pending_requests.iterrows():
            request_rating = dict()
            for rule in self.__rules_structs:
                rule_to_call = self.__rules[rule]
                request_rating[rule] = rule_to_call(pending_request)
            
            #place to save item
            self.db.update_item(dict(sorted(request_rating.items())), request_idx, "Rating", self.db.absence_data)
        
        #for testing purposes only
        #do not use in AWS !!
        #self.__update_db(self.absence_data)


    def set_top_priority_request_status(self, request):
        '''
            set status of first pending request of OU in wich parameter request is 
                based on priorities of rules in "rules_struct"
        '''
        pending_ou_requests = self.db.get_ou_absence_data(request, "Pending")
        pending_ou_requests.set_index(keys="id", inplace=True)

        severities_df = pd.DataFrame((pending_ou_requests["Rating"]).apply(pd.Series), index=pending_ou_requests.index)
        severities_df.sort_values(by=self.__rules_structs, ascending=self.__rules_df_sort, inplace=True)

        top_request = severities_df.iloc[0]
        top_request_absence_data = self.db.absence_data[self.db.absence_data['id'] == top_request.name]
        top_request_absence_data_series = top_request_absence_data.squeeze()

        request_decision = "Accepted"
        for rule_rank in self.__rules_structs:
            #out of treshold - Reject
            #future feature - maybe do helper microrules to really decide if rejected
            if rule_rank in self.__rules_tresholds and \
                (
                    (top_request[rule_rank] == self.__rules_tresholds[rule_rank] and rule_rank != "D") 
                ## treshold has been reached and its not because of leave balance \
                or 
                ## treshold has been reached for time off leave balance
                    (top_request[rule_rank] == self.__rules_tresholds[rule_rank] and rule_rank == "D")
                ):
                    request_decision = "Rejected"   
                    break
                   
        #update request status in Absence data DataFrame
        self.db.update_item(request_decision, top_request_absence_data.index, "Status", self.db.absence_data)

        #update employee leave balance
        if request_decision == "Accepted" and top_request_absence_data_series["AbsenceTypeCode"] == "TIM":
            
            new_leave_balance = self.db.get_employee_info(top_request_absence_data_series, "LeaveBalance") - self.db.get_request_leave_hours(top_request_absence_data_series)
            employee_id = self.db.get_employee_info(top_request_absence_data_series, "EmployeeID")
            employee_idx = self.db.employees[self.db.employees['EmployeeID'] == employee_id].index
            self.db.update_item(new_leave_balance, employee_idx, "LeaveBalance", self.db.employees)

    def absence_requests_handler(self):
        '''
            handle all pending requests until there is none left
        '''
        pending_request_indices = []
        print(self.db.absence_data)
        print(self.db.employees)
        for index, request in self.db.get_requests(status = "Pending").iterrows():
            pending_request_indices.append(index)
            self.rating_function()
            self.set_top_priority_request_status(request)

        #self.db.update_db(self.db.absence_data)
        #self.db.update_db(self.db.employees)
        print(self.db.absence_data)
        print(self.db.employees)
        return self.db.absence_data


if __name__ == "__main__":
    path_absence_table = "back-end/src/data/jsons/absence_data-3.json"
    path_teams_table = "back-end/src/data/jsons/teams_table.json"
    path_employees_table = "back-end/src/data/jsons/employees_table.json"
    path_jobs_table = "back-end/src/data/jsons/jobs_table.json"
    path_absence_type_table = "back-end/src/data/jsons/absence_type.json"

    ars = ARS(path_absence_table, path_teams_table, path_employees_table, path_jobs_table, path_absence_type_table)
    result = ars.absence_requests_handler()

