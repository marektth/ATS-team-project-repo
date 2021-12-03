import unittest

import numpy as np
import pandas as pd
from pandas.util.testing import assert_frame_equal
from src.Absence_rating_system.Data_handler import DBHandler


class TestDataHandler(unittest.TestCase):
    def setUp(self):
        
        self.path_absence_table = "tests/ARS_test_data/test_absence_data.json"
        self.path_teams_table = "tests/ARS_test_data/test_teams_table.json"
        self.path_employees_table = "tests/ARS_test_data/test_employees_table.json"
        self.path_jobs_table = "tests/ARS_test_data/test_jobs_table.json"
        self.path_absence_type_table = "tests/ARS_test_data/test_absence_type.json"

        self.dHandler = DBHandler(self.path_absence_table, self.path_teams_table,
                       self.path_employees_table, self.path_jobs_table, 
                       self.path_absence_type_table)

        self.request = {
            "id": 1,
            "EmployeeID": 96,
            "DateOfAbsence": "24/10/2021",
            "Status": "Pending",
            "Rating": 2
        }
        self.request_pending = pd.DataFrame(self.request,index=[1])
        self.request_pending = self.request_pending.reset_index(drop=True)
        self.request_series = pd.Series(self.request)

    def test_get_requests(self):  
        output = self.dHandler.get_requests(status = "Pending")
        assert_frame_equal(output.reset_index(drop=True), self.request_pending.reset_index(drop=True))

    def test_get_ouid_of_request(self):
        input_ouid = self.dHandler.get_ouid_of_request(self.request_series)
        self.assertEqual(input_ouid, 7)

    def test_get_min_capacity_ou(self):
        input_ouid = self.dHandler.get_min_capacity_ou(self.request_series)
        self.assertEqual(input_ouid, 1)

    def test_get_min_same_job_treshold(self):
        input_threshold = self.dHandler.get_min_same_job_treshold(self.request_series)
        self.assertEqual(input_threshold, 0)

    def test_get_employee_info(self):
        input_info = self.dHandler.get_employee_info(self.request_series)
        output = {
            "EmployeeID": 96,
            "EmployeeName": "jax barker",
            "EmploymentNumber": 0,
            "OUID": 7,
            "LeaveBalance": 8
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
        output = {
            "id": 0,
            "EmployeeID": 54,
            "DateOfAbsence": "23/10/2021",
            "Status": "Accepted",
            "Rating": 1
        }
        output_data = pd.DataFrame(output, index=[0])
        #status_of_absence is All
        assert_frame_equal(output_data.reset_index(drop=True), 
                            input_data.reset_index(drop=True),
                            status_of_absence = "All")



    def test_get_ou_same_job_employees(self):
        input_same_job = self.dHandler.get_ou_same_job_employees(self.request_series)
        data = {'EmployeeID':[54, 96],
                'EmployeeName':['axel style', 'jax barker'],
                'EmploymentNumber':[0, 0],
                'OUID':[7, 7],
                'LeaveBalance': [0, 8]}
        output_same_job = pd.DataFrame(data)
        assert_frame_equal(output_same_job.reset_index(drop=True), input_same_job.reset_index(drop=True))

    def test_get_ou_same_job_absence(self):
        input_same_job_absence = self.dHandler.get_ou_same_job_absence(self.request_series)
        data = {
            "id": 0,
            "EmployeeID": 54,
            "DateOfAbsence": "23/10/2021",
            "Status": "Accepted",
            "Rating": 1
        }
        output_same_job_absence = pd.DataFrame(data, index=[0])
        assert_frame_equal(output_same_job_absence.reset_index(drop=True), input_same_job_absence.reset_index(drop=True))

    def test_convert_to_dayofyear(self):
        request = self.dHandler.convert_to_dayofyear(self.request_pending,
                                                      column_to_convert='DateOfAbsence',
                                                      column_to_add='DayOfYear')
        exp_out = {
            "id": 1,
            "EmployeeID": 96,
            "DateOfAbsence": "24/10/2021",
            "Status": "Pending",
            "Rating": 2,
            "DayOfYear": 297,  
        }
        exp_out = pd.DataFrame(exp_out, index=[1])
        assert_frame_equal(request.reset_index(drop=True), exp_out.reset_index(drop=True))

    # def test_rule_min_capacity_treshold(self):
    #     input_rule_min_capacity = self.ars.rule_min_capacity_treshold(self.request_series)
    #     self.assertEqual(input_rule_min_capacity, 0)
 

if __name__ == '__main__':
    unittest.main()
