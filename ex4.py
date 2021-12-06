##############################################################
# File: ex4.py
# Writer: <Ido Shalom>
# Exercise: intro2cs ex4 2021-2022
# Description: will be inside the README.py file.
##############################################################

from sudoku_helper import *


################################################
######### Start functions in exercises #########
################################################


# 1. Check if board is complete
def sudoku_iscomplete(board):
    for row in board:
        for cell in row:
            if cell == 0:
                return False
    return True


# 2. Return the 3*3 square covering x,y
def sudoku_square3x3(board, x, y):
    x -= x % 3                                         # remove remainder to get the
    y -= y % 3                                         # first element in the square.
    square = []                                        # for the result.
    for i in range(3):                                 # runs on rows.
        square.append([])                              # create the 3x3 square.
        for j in range(3):                             # runs on columns.
            square[i].append(board[x + i][y + j])      # copy the square.
    return square


# 3. Get available options of a position
def sudoku_options(board, x, y, diag=False):
    options = {1, 2, 3, 4, 5, 6, 7, 8, 9}
    for row in range(9):
        if row == x:                                    # skip the current cell.
            continue
        options.discard(board[row][y])                  # remove the numbers in the column from options.
    for col in range(9):
        if col == y:                                    # skip the current cell.
            continue
        options.discard(board[x][col])                  # remove the numbers in the row from options.
    square = sudoku_square3x3(board, x, y)              # get the current 3x3 square.
    for row_s in range(3):
        for col_s in range(3):
            if row_s == x % 3 and col_s == y % 3:
                continue
            options.discard(square[row_s][col_s])
    if diag:
        sudoku_option_diag(board, x, y, options)        # helper function.
    return options


# 4. find all positions which have one option to fill
def find_all_unique(board, diag=False):
    unique_cells = []                                                 # for the final outcome.
    for i in range(9):                                                # runs on in index in rows.
        for j in range(9):                                            # runs on in index columns.
            if board[i][j] == 0:                                      # check if the value is 0.
                options = list(sudoku_options(board, i, j, diag))     # get the options for specific cell.
                if len(options) == 1:                                 # check if option unique.
                    val = options[0]                                  # the unique option.
                    unique_cells.append((i, j, val))                  # all the unique options.
    return unique_cells


# 5. Check if board is valid
def sudoku_isvalid(board, diag=False):
    for i in range(9):
        for j in range(9):
            if board[i][j] != 0:                                      # check if value not 0.
                options = sudoku_options(board, i, j, diag)
                if board[i][j] not in options:                        # check if the cell not in options.
                    return False
    return True


# 6. Find squares with no option to fill
def find_all_conflicts(board, diag=False):
    all_conflicts = []
    for i in range(9):
        for j in range(9):
            options = sudoku_options(board, i, j, diag)
            if len(options) == 0:                          # if length is 0,there is no valid options for this cell.
                all_conflicts.append((i, j))               # gives all the conflicts.
    return all_conflicts


# 7. Add square if possible:
def add_square(board, i, j, val, diag=False):
    if val in sudoku_options(board, i, j, diag):           # if value in options, the value is valid
        board[i][j] = val                                  # add the value to the board.
        return True
    else:
        print("Error! Value is in conflict with current board")
        return False


# 8. Iteratively fill the board with unique options
def fill_board(board, diag=False):
    some_cell_changed = False                           # flag to check if some cells has been changed.
    non_zero_cells = 0                                  # count the non zero cells to check if the board is completed.
    for i in range(9):
        for j in range(9):
            if board[i][j] == 0:
                options = list(sudoku_options(board, i, j, diag))
                if len(options) == 0:                    # if length is 0,there is no valid options for this cell.
                    print("Error! current sudoku leads to inconsistencies. Must delete values")
                    return False
                elif len(options) == 1:                 # if length is 1, fill the only option.
                    board[i][j] = options[0]
                    some_cell_changed = True            # changed the flag when the cell changes.
                    non_zero_cells += 1
            else:
                non_zero_cells += 1                     # add to count if the cell already have value.
    if some_cell_changed:                               # repeat the action recursively.
        return fill_board(board, diag)
    if non_zero_cells == 81:
        print("Success! sudoku solved")
    else:
        print("Sudoku partially solved")
    return True


# Additional helper functions below:
# ..

def sudoku_option_diag(board, x, y, options):      # helper function question 3.
    if x == y:                                     # check if current cell in main diagonal.
        for i in range(9):
            if i == x:
                continue
            options.discard(board[i][i])
    if x + y == 8:                                 # check if current cell in second diagonal.
        for i in range(9):
            if i == x:
                continue
            options.discard(board[i][8 - i])







