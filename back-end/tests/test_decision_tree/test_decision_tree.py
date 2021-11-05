
import unittest
import pandas as pd
from pandas.util.testing import assert_frame_equal # <-- for testing dataframes

from src.decision_tree import decision_tree as dt


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

if __name__ == '__main__':
    unittest.main()

