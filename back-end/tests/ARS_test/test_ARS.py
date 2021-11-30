import unittest
import pandas as pd
from src.deciding_algorithm.ARS import ARS
from pandas.util.testing import assert_frame_equal
import numpy as np


class TestARS(unittest.TestCase):
    def setUp(self):
        
        self.path_absence_table = "tests/ARS_test_data/test_absence_data.json"
        self.path_teams_table = "src/data/jsons/teams_table.json"
        self.path_employees_table = "src/data/jsons/employees_table.json"
        self.path_jobs_table = "src/data/jsons/jobs_table.json"
        self.ars = ARS(self.path_absence_table, self.path_teams_table,
                self.path_employees_table, self.path_jobs_table)

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
        output = self.ars._ARS__get_requests(status = "Pending")
        assert_frame_equal(output.reset_index(drop=True), self.request_pending.reset_index(drop=True))

    def test_get_ouid_of_request(self):
        input_ouid = self.ars._ARS__get_ouid_of_request(self.request_series)
        self.assertEqual(input_ouid, 7)

    def test_get_min_capacity_ou(self):
        input_ouid = self.ars._ARS__get_min_capacity_ou(self.request_series)
        self.assertEqual(input_ouid, 4)

    def test_get_min_same_job_treshold(self):
        input_threshold = self.ars._ARS__get_min_same_job_treshold(self.request_series)
        self.assertEqual(input_threshold, 1)

    def test_get_employee_info(self):
        input_info = self.ars._ARS__get_employee_info(self.request_series)
        output = {
            "EmployeeID": 96,
            "EmployeeName": "jax barker",
            "EmploymentNumber": 0,
            "OUID": 7
        }
        output_df = pd.DataFrame(output, index=[0])
        assert_frame_equal(output_df.reset_index(drop=True), input_info.reset_index(drop=True))

    def test_get_ou_employees(self):
        input_id = self.ars._ARS__get_ou_employees(self.request_series)
        print(type(input_id))
        input_id = input_id.tolist()
        output = [79, 69, 62, 54, 96]
        print(type(output))

        self.assertEqual(input_id, output)

    def test_get_size_of_ou(self):
        pass

    def test_get_ou_absence_data(self):
        pass

    def test_get_ou_same_job_employees(self):
        pass

    def test_get_ou_same_job_absence(self):
        pass

    def test_convert_to_dayofyear(self):
        request = self.ars._ARS__convert_to_dayofyear(self.request_pending,
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

        

if __name__ == '__main__':
    unittest.main()
