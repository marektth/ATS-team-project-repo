
import unittest
import pandas as pd
from pandas.util.testing import assert_frame_equal # <-- for testing dataframes
import decision_tree as dt

class TestDecisiontree(unittest.TestCase):
    def test_status_column_add(self):
        dum = pd.read_csv("dummy_df.csv")
        right = pd.read_csv("dummy_df_1.csv")
        test = dt.status_column_add(dum)
        assert_frame_equal(test, right)

    # def test_two(self):
    #     x = "hello"
    #     assert hasattr(x, "check")
if __name__ == '__main__':
    unittest.main()