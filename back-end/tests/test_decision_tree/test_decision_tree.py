import unittest
import pandas as pd
from pandas.util.testing import assert_frame_equal
import decision_tree as dt

class TestDecisiontree(unittest.TestCase):
    def test_status_column_add(self):
        input_df = {'': [0, 1],
                     "Status": ["Accepted", "Rejected"]}
        input_df = pd.DataFrame(input_df)

        output_df = {'': [0, 1],
                    "Status": [1, 0],
                    "Overlap": [0,0]}

        output_df = pd.DataFrame(output_df)

        df_to_test = dt.status_column_add(input_df)
        assert_frame_equal(df_to_test, output_df)

    def test_converter(self):
        input_df = {'': [0, 1],
                     "StartDate": ["20/01/2021", "24/04/2021"],
                     "EndDate": ["23/01/2021", "28/04/2021"]}
        input_df = pd.DataFrame.from_dict(input_df)

        output_df = {'': [0, 1],
                    "StartDate": [20210120, 20210424],
                    "EndDate": [20210123, 20210428]}
        
        output_df = pd.DataFrame.from_dict(output_df)

        conversion_test = dt.converter(input_df)

        assert_frame_equal(conversion_test, output_df)

    def test_overlap_dates_finder(self):
        input_df = {'': [0, 1],
                     "StartDate": [20210729, 20210727],
                     "EndDate": [20210731, 20210804],
                     "Status": [1,1],
                     "Overlap": [0,0]}
        input_df = pd.DataFrame.from_dict(input_df)

        output_df = {'': [0, 1],
                    "StartDate": [20210729, 20210727],
                    "EndDate": [20210731, 20210804],
                    "Status": [0,0],
                    "Overlap": [1,1]}
        
        output_df = pd.DataFrame.from_dict(output_df)

        overlap_dates_finder_test = dt.overlap_dates_finder(input_df)

        assert_frame_equal(overlap_dates_finder_test, output_df)

    def test_decision_tree(self):
        input_df = {'': [0, 1, 2, 3],
                     "Overlap": [0, 0, 1, 1],
                     "Status": [1, 1, 0, 0]}
        input_df = pd.DataFrame(input_df)
        
        input_wrong_df = {'': [],
                     "Overlap": [],
                     "Status": []}
        input_wrong_df = pd.DataFrame(input_wrong_df)

        decision_tree_test = dt.decision_tree(input_df)
        decision_tree_wrong_test = dt.decision_tree(input_wrong_df)
        
        self.assertEqual(decision_tree_wrong_test, 0)
        self.assertEqual(decision_tree_test, 1)

if __name__ == '__main__':
    unittest.main()
