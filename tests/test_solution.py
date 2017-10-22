import solution
import unittest
import json
import os

TEST_DATA_PATH = os.path.join(os.path.dirname(__file__), 'test_data.json')


class TestGridValues(unittest.TestCase):
    def setUp(self):
        with open(TEST_DATA_PATH) as f:
            self.test_data = json.load(f)

        self.basic_string = self.test_data['basic_puzzle']['unsolved_string']

    def test_grid_values1(self):
        expected = self.test_data['basic_puzzle']['unsolved_dict']
        self.assertDictEqual(expected, solution.grid_values(
            self.basic_string))


class TestNakedTwins(unittest.TestCase):
    def setUp(self):
        with open(TEST_DATA_PATH) as f:
            self.test_data = json.load(f)
        self.naked_twins_data = self.test_data['naked_twins']

    def test_naked_twins(self):
        before_naked_twins_1 = self.naked_twins_data['before_naked_twins_1']
        possible_solutions_1 = self.naked_twins_data['possible_solutions_1']
        self.assertIn(solution.naked_twins(before_naked_twins_1),
                      possible_solutions_1,
                      "naked_twins function produced an unexpected board.")

    def test_naked_twins2(self):
        before_naked_twins_2 = self.naked_twins_data['before_naked_twins_2']
        possible_solutions_2 = self.naked_twins_data['possible_solutions_2']
        self.assertTrue(solution.naked_twins(before_naked_twins_2) in possible_solutions_2,
                        "Your naked_twins function produced an unexpected board.")


class TestEliminate(unittest.TestCase):
    def setUp(self):
        with open(TEST_DATA_PATH) as f:
            self.test_data = json.load(f)
        basic_puzzle_data = self.test_data['basic_puzzle']

        self.values_before = basic_puzzle_data['unsolved_dict']
        self.initial_solved = basic_puzzle_data['initial_solved_boxes']
        self.peers = self.test_data['general']['peers']

    def test_eliminate(self):
        """Test that the value of each solved box is removed from the values of
        all its peers
        """
        values_after = solution.eliminate(self.values_before)
        for box in self.initial_solved:
            peer_vals = []
            for p in self.peers[box]:
                peer_vals += values_after[p]
        self.assertNotIn(values_after[box], peer_vals)


class TestOnlyChoice(unittest.TestCase):
    def setUp(self):
        with open(TEST_DATA_PATH) as f:
            self.test_data = json.load(f)

        self.values_before = self.test_data['basic_puzzle']['unsolved_dict']
        # remove '1' from possibilities in all boxes for row A
        row_A = ["A1", "A2", "A3", "A4", "A5", "A6", "A7", "A8", "A9"]
        for box in row_A:
            self.values_before[box] = self.values_before[box].replace('1', '')

        # add '1' as a possibility to ONLY 'A1'
        self.values_before['A1'] = self.values_before['A1'] + '1'

    def test_only_choice(self):
        """Test box that is only choice for a given value in a unit is assigned
        that value
        """
        values_after = solution.only_choice(self.values_before)
        self.assertEqual('1', values_after['A1'])


class TestReducePuzzle(unittest.TestCase):
    def setUp(self):
        with open(TEST_DATA_PATH) as f:
            self.test_data = json.load(f)

        self.values_before = self.test_data['basic_puzzle']['unsolved_dict']

    def test_reduce_puzzle_no_value(self):
        """Test reduce_puzzle return false when a box has no possible values
        """
        # make box with no values
        self.values_before['I5'] = ''
        self.assertFalse(solution.reduce_puzzle(self.values_before))


class TestDiagonalSudoku(unittest.TestCase):
    def setUp(self):
        with open(TEST_DATA_PATH) as f:
            self.test_data = json.load(f)

    def test_solve(self):
        diagonal_grid = self.test_data['diagonal_sudoku']['diagonal_grid']
        solved_grid = self.test_data['diagonal_sudoku']['solved_diag_sudoku']
        self.assertEqual(solution.solve(diagonal_grid), solved_grid)


if __name__ == '__main__':
    unittest.main()
