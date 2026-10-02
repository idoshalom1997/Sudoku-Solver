import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sudoku import (add_square, fill_board, find_all_conflicts, find_all_unique,
                    sudoku_iscomplete, sudoku_isvalid, sudoku_options, sudoku_square3x3)

SOLVED = [[2, 5, 8, 7, 3, 6, 9, 4, 1],
          [6, 1, 9, 8, 2, 4, 3, 5, 7],
          [4, 3, 7, 9, 1, 5, 2, 6, 8],
          [3, 9, 5, 2, 7, 1, 4, 8, 6],
          [7, 6, 2, 4, 9, 8, 1, 3, 5],
          [8, 4, 1, 6, 5, 3, 7, 2, 9],
          [1, 8, 4, 3, 6, 9, 5, 7, 2],
          [5, 7, 6, 1, 4, 2, 8, 9, 3],
          [9, 2, 3, 5, 8, 7, 6, 1, 4]]


def board_with_holes(cells):
    board = [row[:] for row in SOLVED]
    for i, j in cells:
        board[i][j] = 0
    return board


class SudokuTests(unittest.TestCase):
    def test_complete_board(self):
        self.assertTrue(sudoku_iscomplete(SOLVED))
        self.assertFalse(sudoku_iscomplete(board_with_holes([(4, 4)])))

    def test_square(self):
        self.assertEqual(sudoku_square3x3(SOLVED, 4, 7), [[4, 8, 6], [1, 3, 5], [7, 2, 9]])

    def test_options_of_single_hole(self):
        self.assertEqual(sudoku_options(board_with_holes([(4, 4)]), 4, 4), {9})

    def test_valid_and_invalid_board(self):
        self.assertTrue(sudoku_isvalid(SOLVED))
        broken = [row[:] for row in SOLVED]
        broken[0][0] = 5
        self.assertFalse(sudoku_isvalid(broken))

    def test_unique_cells_and_conflicts(self):
        board = board_with_holes([(0, 0), (8, 8)])
        self.assertEqual(sorted(find_all_unique(board)), [(0, 0, 2), (8, 8, 4)])
        self.assertEqual(find_all_conflicts(board), [])

    def test_add_square_rejects_conflict(self):
        board = board_with_holes([(4, 4)])
        self.assertFalse(add_square(board, 4, 4, 1))
        self.assertTrue(add_square(board, 4, 4, 9))

    def test_fill_board_solves(self):
        board = board_with_holes([(i, i) for i in range(9)] + [(0, 8), (8, 0)])
        self.assertTrue(fill_board(board))
        self.assertEqual(board, SOLVED)


if __name__ == "__main__":
    unittest.main()
