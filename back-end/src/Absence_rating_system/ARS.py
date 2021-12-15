from src.Absence_rating_system.Data_handler import DBHandler
import pandas as pd
import time

class ARS():
    '''
    If first import is not working then try ths one from Data_handler import DBHandler    
    '''
    def __init__(self, absence_data, teams, employees, jobs, absence_type, rules):

        self.db = DBHandler(absence_data, teams, employees, jobs, absence_type, rules)

        self.__rules = self.db.get_rules_by_keys()
        self.__rules_structs, self.__rules_df_sort = self.db.get_rules_with_order()


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

        #format dates
        ou_absence_data = self.db.format_absence_dates(ou_absence_data)
        request = self.db.format_absence_dates(request)

        #number of employees that are off on the day of requests
        employee_absence_overlap_no = 0

        #iterate over accepted timeoffs
        for _, absence_data in ou_absence_data.iterrows():
            #if employee has accepted timeoff in same day as new request, increment counter
            if self.db.get_no_overlapping_days(absence_data, request) > 0:
                employee_absence_overlap_no += 1
            
        
        if normalized:
            return employee_absence_overlap_no/self.db.get_size_of_ou(request)
        else:
            return employee_absence_overlap_no


    def rule_min_capacity_threshold(self, request):
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

        #format dates
        same_job_absence_data = self.db.format_absence_dates(same_job_absence_data)
        request = self.db.format_absence_dates(request)

        #number of employees that are off on the day of requests
        employee_absence_overlap_no = 0

        #iterate over accepted timeoffs
        for _, absence_data in same_job_absence_data.iterrows():
            #if employee has accepted timeoff in same day as new request, increment counter
            #if employee has accepted timeoff in same day as new request, increment counter
            if self.db.get_no_overlapping_days(absence_data, request) > 0:
                employee_absence_overlap_no += 1
                
        
        if normalized:
            return employee_absence_overlap_no/self.db.get_size_of_ou(request)
        else:
            return employee_absence_overlap_no



    def rule_min_same_job_threshold(self, request):
        '''
            returns if absent same job employees treshhold is exceeded
        '''
        min_same_job_tresh = self.db.get_min_same_job_threshold(request)
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
        

    def rating_function(self, request):
        '''
            rate all pending requests based on rules specified in rules priority
            saves ratings in dataframe
        '''
        
        ou_pending_requests = self.db.get_ou_absence_data(request, status_of_absence="Pending")
        for request_idx, pending_request in ou_pending_requests.iterrows():
            request_rating = dict()
            for rule in self.__rules:
                request_rating[rule["key"]] = getattr(ars, rule["function"])(pending_request)
            
            #save request rating
            self.db.update_item(dict(sorted(request_rating.items())), request_idx, "Rating", self.db.absence_data)

    def get_top_priority_request(self, request):
        pending_ou_requests = self.db.get_ou_absence_data(request, "Pending")
        pending_ou_requests.set_index(keys="id", inplace=True)

        severities_df = pd.DataFrame((pending_ou_requests["Rating"]).apply(pd.Series), index=pending_ou_requests.index)



        severities_df.sort_values(by=self.__rules_structs, ascending=self.__rules_df_sort, inplace=True)

        top_request = severities_df.iloc[0]
        top_request_absence_data = self.db.absence_data[self.db.absence_data['id'] == top_request.name]

        return top_request, top_request_absence_data.squeeze()



    def determine_top_priority_status(self, top_request):
        request_status = "Accepted"
        status_resolution = "OK"
        for rule_rank in self.__rules_structs:
            #out of treshold - Reject
            #future feature - maybe do helper microrules to really decide if rejected
            threshold = self.db.get_rule_threshold_by_key(rule_rank)
            if not pd.isnull(threshold) and \
                (
                    (top_request[rule_rank] == threshold and rule_rank != "D") 
                ## treshold has been reached and its not because of leave balance \
                or 
                ## treshold has been reached for time off leave balance
                    (top_request[rule_rank] == threshold and rule_rank == "D")
                ):
                    request_status = "Rejected"
                    status_resolution = self.db.get_rule_status_failed_resolution(rule_rank)
                    break

        return request_status, status_resolution


    def set_ou_requests_statuses(self, request):
        '''
            set status of first pending request of OU in wich parameter request is 
                based on priorities of rules in "rules_struct"
        '''
        for _, pending_request in self.db.get_ou_absence_data(request, "Pending").iterrows():
            self.rating_function(pending_request)
            top_request, top_request_absence_data = self.get_top_priority_request(pending_request)
            status_to_set, status_resolution = self.determine_top_priority_status(top_request)

            # update request status in absence_data DataFrame
            self.db.update_item(status_to_set, top_request_absence_data.name, "Status", self.db.absence_data)
            self.db.update_item(status_resolution, top_request_absence_data.name, "StatusResolution", self.db.absence_data)

            # update employee leave balance if request accepted and its just timeoff
            if status_to_set == "Accepted" and top_request_absence_data['AbsenceTypeCode'] == "TIM":
                new_leave_balance = self.db.get_employee_info(top_request_absence_data, "LeaveBalance") - self.db.get_request_leave_hours(top_request_absence_data)
                employee_idx = self.db.employees[self.db.employees['EmployeeID'] == top_request_absence_data['EmployeeID']].index
                self.db.update_item(new_leave_balance, employee_idx, "LeaveBalance", self.db.employees)


    def absence_requests_handler(self):
        '''
            handle all pending requests until there is none left
        '''
        all_pending_requests = self.db.get_requests(status = "Pending")

        #set statuses to whole OU at time
        while not all_pending_requests.empty:
            start_time = time.time()

            old_request_no = all_pending_requests.shape[0]

            request = all_pending_requests.iloc[0]
            request_ouid = self.db.get_ouid_of_request(request)
            self.set_ou_requests_statuses(request)

            # get fresh data
            all_pending_requests = self.db.get_requests(status = "Pending")
            new_request_no = all_pending_requests.shape[0]

            # if nothing changed, break while loop to prevent infinite loop
            # safety measure
            if (old_request_no == new_request_no):
                break

            self.db.set_ou_rating_duration(request_ouid, start_time)

        self.db.update_db(self.db.teams, self.db.teams_data_path)
        ## do not forget to save also teams table on AWS!
        return self.db.absence_data


if __name__ == "__main__":
    path_absence_table = "back-end/src/data/jsons/absence_data.json"
    path_teams_table = "back-end/src/data/jsons/teams_table.json"
    path_employees_table = "back-end/src/data/jsons/employees_table.json"
    path_jobs_table = "back-end/src/data/jsons/jobs_table.json"
    path_absence_type_table = "back-end/src/data/jsons/absence_type.json"
    path_rules_table = "back-end/src/data/jsons/rules_table.json"

    ars = ARS(path_absence_table, path_teams_table, path_employees_table, path_jobs_table, path_absence_type_table, path_rules_table)
    result = ars.absence_requests_handler()
    
   

