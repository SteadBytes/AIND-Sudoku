import solution
import unittest
import json
import os
TEST_DATA_PATH = os.path.join(os.path.dirname(__file__), 'test_data.json')
with open(TEST_DATA_PATH) as f:
    test_data = json.load(f)


class TestNakedTwins(unittest.TestCase):
    before_naked_twins_1 = test_data['naked_twins']['before_naked_twins_1']
    possible_solutions_1 = test_data['naked_twins']['possible_solutions_1']

    before_naked_twins_2 = test_data['naked_twins']['before_naked_twins_2']
    possible_solutions_2 = test_data['naked_twins']['possible_solutions_2']

    def test_naked_twins(self):
        self.assertTrue(solution.naked_twins(self.before_naked_twins_1) in self.possible_solutions_1,
                        "Your naked_twins function produced an unexpected board.")

    def test_naked_twins2(self):
        self.assertTrue(solution.naked_twins(self.before_naked_twins_2) in self.possible_solutions_2,
                        "Your naked_twins function produced an unexpected board.")


class TestDiagonalSudoku(unittest.TestCase):
    diagonal_grid = test_data['diagonal_sudoku']['diagonal_grid']
    solved_diag_sudoku = test_data['diagonal_sudoku']['solved_diag_sudoku']

    def test_solve(self):
        self.assertEqual(solution.solve(self.diagonal_grid),
                         self.solved_diag_sudoku)


if __name__ == '__main__':
    unittest.main()
