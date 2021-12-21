import json as json
import unittest

import numpy as np
import pandas as pd
from numpy.testing import assert_array_equal
from pandas.testing import assert_frame_equal, assert_series_equal
from src.Absence_rating_system.ARS import ARS


class TestARS(unittest.TestCase):
    def setUp(self):
        
        self.path_absence_table = "tests/ARS_test_data/test_absence_data.json"
        self.path_teams_table = "tests/ARS_test_data/test_teams_table.json"
        self.path_employees_table = "tests/ARS_test_data/test_employees_table.json"
        self.path_jobs_table = "tests/ARS_test_data/test_jobs_table.json"
        self.path_absence_type_table = "tests/ARS_test_data/test_absence_type.json"
        self.path_test_request = "tests/ARS_test_data/test_request.json"
        self.path_rules_table =  "tests/ARS_test_data/rules_table.json"

        self.ars = ARS(self.path_absence_table, self.path_teams_table,
                       self.path_employees_table, self.path_jobs_table, 
                       self.path_absence_type_table, self.path_rules_table)

        with open(self.path_test_request) as f:
            json_data = json.load(f)
        self.request_pending = pd.DataFrame(json_data, index=[1])
        self.request_series = pd.Series(json_data[0])



    def test_rule_min_capacity_treshold(self):
        input_rule_min_capacity = self.ars.rule_min_capacity_threshold(self.request_series)
        self.assertEqual(input_rule_min_capacity, 0)

    def test_rule_set_absence_type_priority(self):
        input_rule_absence_priority = self.ars.rule_set_absence_type_priority(self.request_series)
        self.assertEqual(input_rule_absence_priority, 3)

    def test_absence_requests_handler1(self):
        '''
            Test case for testing 2 employees with requested timeoff at the different
            days. One employee has leave balance 0 hours and second 8 hours.
        '''
        self.path_absence_table_case1 = "tests/ARS_test_data/ARS_test_case1/test_absence_data.json"
        self.ars = ARS(self.path_absence_table_case1, self.path_teams_table,
                       self.path_employees_table, self.path_jobs_table, 
                       self.path_absence_type_table, self.path_rules_table)
        
        input_case1 = self.ars.absence_requests_handler()
        self.path_absence_table_case1_correct = "tests/ARS_test_data/ARS_test_case1/test_absence_data_correct.json"
        with open(self.path_absence_table_case1_correct) as f:
            json_data = json.load(f)
        output_case1_correct = pd.DataFrame(json_data)

        input_case1_status = input_case1["Status"]
        output_case1_correct_status = output_case1_correct["Status"]

        assert_series_equal(input_case1_status, output_case1_correct_status)

    def test_absence_requests_handler2(self):
        '''
            Test case for testing 2 employees with requested timeoff at the same
            days. One employee has leave balance 0 hours and second 8 hours.
        '''
        self.path_absence_table_case2 = "tests/ARS_test_data/ARS_test_case2/test_absence_data.json"
        self.path_jobs_table_case2 = "tests/ARS_test_data/ARS_test_case2/test_jobs_table.json"
        self.ars = ARS(self.path_absence_table_case2, self.path_teams_table,
                       self.path_employees_table, self.path_jobs_table_case2, 
                       self.path_absence_type_table, self.path_rules_table)
        
        input_case2 = self.ars.absence_requests_handler()
        self.path_absence_table_case2_correct = "tests/ARS_test_data/ARS_test_case2/test_absence_data_correct.json"
        with open(self.path_absence_table_case2_correct) as f:
            json_data = json.load(f)
        output_case2_correct = pd.DataFrame(json_data)

        input_case2_status = input_case2["Status"]
        output_case2_correct_status = output_case2_correct["Status"]

        assert_series_equal(input_case2_status, output_case2_correct_status)

    def test_absence_requests_handler3(self):
        '''
            Test case for testing 2 employees with one requesting timeoff and second requesting
            parental holiday at the same day. Both employees have leave balance 8 hours.
        '''
        self.path_absence_table_case3 = "tests/ARS_test_data/ARS_test_case3/test_absence_data.json"
        self.path_jobs_table_case3 = "tests/ARS_test_data/ARS_test_case3/test_jobs_table.json"
        self.path_employees_table_case3 = "tests/ARS_test_data/ARS_test_case3/test_employees_table.json"
        self.ars = ARS(self.path_absence_table_case3, self.path_teams_table,
                       self.path_employees_table_case3, self.path_jobs_table_case3, 
                       self.path_absence_type_table, self.path_rules_table)
        
        input_case3 = self.ars.absence_requests_handler()
        self.path_absence_table_case3_correct = "tests/ARS_test_data/ARS_test_case3/test_absence_data_correct.json"
        with open(self.path_absence_table_case3_correct) as f:
            json_data = json.load(f)
        output_case3_correct = pd.DataFrame(json_data)

        input_case3_status = input_case3["Status"]
        output_case3_correct_status = output_case3_correct["Status"]

        assert_series_equal(input_case3_status, output_case3_correct_status)

    def test_absence_requests_handler4(self):
        '''
            Test case for testing 2 employees with both of them requesting
            parental holiday at the different days.
        '''
        self.path_absence_table_case4 = "tests/ARS_test_data/ARS_test_case4/test_absence_data.json"
        self.path_jobs_table_case4 = "tests/ARS_test_data/ARS_test_case4/test_jobs_table.json"
        self.path_employees_table_case4 = "tests/ARS_test_data/ARS_test_case4/test_employees_table.json"
        self.ars = ARS(self.path_absence_table_case4, self.path_teams_table,
                       self.path_employees_table_case4, self.path_jobs_table_case4, 
                       self.path_absence_type_table, self.path_rules_table)
        
        input_case4 = self.ars.absence_requests_handler()
        self.path_absence_table_case4_correct = "tests/ARS_test_data/ARS_test_case4/test_absence_data_correct.json"
        with open(self.path_absence_table_case4_correct) as f:
            json_data = json.load(f)
        output_case4_correct = pd.DataFrame(json_data)

        input_case4_status = input_case4["Status"]
        output_case4_correct_status = output_case4_correct["Status"]

        assert_series_equal(input_case4_status, output_case4_correct_status)

    def test_absence_requests_handler5(self):
        '''
            Test case for testing 2 employees with one of them requesting
            parental holiday and second one requesting special holiday at the different days.
        '''
        self.path_absence_table_case5 = "tests/ARS_test_data/ARS_test_case5/test_absence_data.json"
        self.path_jobs_table_case5 = "tests/ARS_test_data/ARS_test_case5/test_jobs_table.json"
        self.path_employees_table_case5 = "tests/ARS_test_data/ARS_test_case5/test_employees_table.json"
        self.ars = ARS(self.path_absence_table_case5, self.path_teams_table,
                       self.path_employees_table_case5, self.path_jobs_table_case5, 
                       self.path_absence_type_table, self.path_rules_table)
        
        input_case5 = self.ars.absence_requests_handler()
        self.path_absence_table_case5_correct = "tests/ARS_test_data/ARS_test_case5/test_absence_data_correct.json"
        with open(self.path_absence_table_case5_correct) as f:
            json_data = json.load(f)
        output_case5_correct = pd.DataFrame(json_data)

        input_case5_status = input_case5["Status"]
        output_case5_correct_status = output_case5_correct["Status"]

        assert_series_equal(input_case5_status, output_case5_correct_status)


 

if __name__ == '__main__':
    unittest.main()
