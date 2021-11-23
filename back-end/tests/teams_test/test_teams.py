import unittest
import pandas as pd
import teams as tm

class TestTeams(unittest.TestCase):
    def test_unique_numbers(self):
        input = 10
        output = tm.unique_numbers(input)
        output_len = len(output)
        output_test = 10
        self.assertEqual(output_len, output_test)

    def test_unique_team_name(self):
        input = 10
        output = tm.unique_team_name(input)
        output_len = len(output)
        output_test = 10
        self.assertEqual(output_len, output_test)



if __name__ == '__main__':
    unittest.main()
