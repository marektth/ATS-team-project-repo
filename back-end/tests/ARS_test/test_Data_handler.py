import json as json
import unittest

import numpy as np
import pandas as pd
from numpy.testing import assert_array_equal
from pandas.testing import assert_frame_equal, assert_series_equal
from src.Absence_rating_system.Data_handler import DBHandler


class TestDataHandler(unittest.TestCase):
    def setUp(self):
        
        self.path_absence_table = "tests/ARS_test_data/test_absence_data.json"
        self.path_teams_table = "tests/ARS_test_data/test_teams_table.json"
        self.path_employees_table = "tests/ARS_test_data/test_employees_table.json"
        self.path_jobs_table = "tests/ARS_test_data/test_jobs_table.json"
        self.path_absence_type_table = "tests/ARS_test_data/test_absence_type.json"
        self.path_test_request = "tests/ARS_test_data/test_request.json"
        self.path_rules_table =  "tests/ARS_test_data/rules_table.json"


        self.dHandler = DBHandler(self.path_absence_table, self.path_teams_table,
                       self.path_employees_table, self.path_jobs_table, 
                       self.path_absence_type_table, self.path_rules_table)

        with open(self.path_test_request) as f:
            json_data = json.load(f)
        self.request_pending = pd.DataFrame(json_data, index=[1])
        self.request_series = pd.Series(json_data[0])

    def test_get_requests(self):  
        output = self.dHandler.get_requests(status = "Pending")
        assert_frame_equal(output, self.request_pending)

    def test_get_ouid_of_request(self):
        input_ouid = self.dHandler.get_ouid_of_request(self.request_series)
        self.assertEqual(input_ouid, 7)

    def test_get_min_capacity_ou(self):
        input_ouid = self.dHandler.get_min_capacity_ou(self.request_series)
        self.assertEqual(input_ouid, 1)

    def test_get_min_same_job_treshold(self):
        input_threshold = self.dHandler.get_min_same_job_threshold(self.request_series)
        self.assertEqual(input_threshold, 0)

    def test_get_employee_info(self):
        input_info = self.dHandler.get_employee_info(self.request_series)
        output = {
            "EmployeeID": 96,
            "EmployeeName": "jax barker",
            "EmploymentNumber": 0,
            "OUID": 7,
            "LeaveBalance": 8,
            "LeaveBalanceDisplay": 8
        }
        output_df = pd.DataFrame(output, index=[0])
        assert_frame_equal(output_df.reset_index(drop=True), input_info.reset_index(drop=True))

    def test_get_ou_employees(self):
        input_id = self.dHandler.get_ou_employees(self.request_series)
        input_id = input_id.tolist()
        output = [79, 69, 62, 54, 96, 192]
        self.assertEqual(input_id, output)

    def test_get_size_of_ou(self):
        input_size = self.dHandler.get_size_of_ou(self.request_series)
        self.assertEqual(input_size, 6)

    def test_get_ou_absence_data(self): 
        #status_of_absence is Accepted, Reqected, Pending
        input_data = self.dHandler.get_ou_absence_data(self.request_series)        
        output_path = "tests/ARS_test_data/test_ou_absence_data.json"
        with open(output_path) as f:
            json_data = json.load(f)
        output_data = pd.DataFrame(json_data, index=[0])
        assert_frame_equal(output_data, 
                            input_data)
        #status_of_absence is All,
        input_data_test_case2 = self.dHandler.get_ou_absence_data(self.request_series,
                                                        status_of_absence = "All")
        output_test_case2 = self.dHandler.absence_data
        assert_frame_equal(output_test_case2.reset_index(drop=True), 
                            input_data_test_case2.reset_index(drop=True))
        
    def test_get_ou_same_job_employees(self):
        #if only_id is False
        input_same_job = self.dHandler.get_ou_same_job_employees(self.request_series)
        data = {'EmployeeID':[54, 96],
                'EmployeeName':['axel style', 'jax barker'],
                'EmploymentNumber':[0, 0],
                'OUID':[7, 7],
                'LeaveBalance': [0, 8],
                "LeaveBalanceDisplay": [0, 8]}
        output_same_job = pd.DataFrame(data)
        assert_frame_equal(output_same_job.reset_index(drop=True), input_same_job.reset_index(drop=True))
        #if only_id is True
        input_same_job_case2 = self.dHandler.get_ou_same_job_employees(self.request_series, only_id=True)
        output_case2 = [54, 96]
        output_case2 = np.array(output_case2, dtype="int64")
        assert_array_equal(input_same_job_case2, output_case2)
       
    def test_get_ou_same_job_absence(self):
        input_same_job_absence = self.dHandler.get_ou_same_job_absence(self.request_series)
        output_path = "tests/ARS_test_data/test_ou_absence_data.json"
        with open(output_path) as f:
            json_data = json.load(f)
        output_same_job_absence = pd.DataFrame(json_data, index=[0])
        assert_frame_equal(output_same_job_absence.reset_index(drop=True), input_same_job_absence.reset_index(drop=True))

    def test_get_absence_type_priority(self):
        input_priority = self.dHandler.get_absence_type_priority(self.request_series)
        self.assertEqual(input_priority, 3)

    def test_get_request_leave_hours(self):
        input_leave_hours = self.dHandler.get_request_leave_hours(self.request_series)
        self.assertEqual(input_leave_hours, 80)

    def test_check_enough_leave_balance(self):
       input_leave_balance = self.dHandler.check_enough_leave_balance(self.request_series)
       self.assertEqual(input_leave_balance, False)


if __name__ == '__main__':
    unittest.main()
