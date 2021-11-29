import pygame
import copy
import random


# Run sudoku game. n is the number of filled squares
def sudoku_action(n=25, diag=False, input_board=None):
    from ex4 import fill_board, add_square, sudoku_options, sudoku_iscomplete

    size = [9,9]  # fixed board
    board, full_board, xy = generate_random_board(n, diag, input_board)

    while True:
        display_sudoku(board, size, xy)  # choose if to display init, current, or solved board !
        if sudoku_iscomplete(board):
            break
        action = input('Choose operation: add <x> <y> <val>, remove <x> <y>, options <x> <y>, solve-unique, show-solution, done').split()

        if action[0] == 'add':
            add_square(board, int(action[1])-1, int(action[2])-1, int(action[3]), diag)
        elif action[0] == 'remove':
            board[int(action[1])-1][int(action[2])-1] = 0
        elif action[0] == 'options':  # get square options
            print("Options: "+"".join(str(sudoku_options(board, int(action[1])-1, int(action[2])-1, diag))))
        # display solution
        elif action[0] == 'solve-unique':
            fill_board(board, diag)
        if action[0] == 'show-solution':  # show full board.
            display_sudoku(full_board, size, xy)
            break
        if action[0] == 'done':
            break
    print('Finished Sudoku')


# Generate a random initial board
def generate_random_board(init_num=25, diag=False, input_grid=None):
    from ex4 import sudoku_isvalid

    if input_grid == None:
        grid = make_board(3, diag)
    else:
        grid = copy.deepcopy(input_grid)
        if not sudoku_isvalid(grid): # check if grid is valid
            print("Error! entered invalid Sudoku board")
    full_grid = copy.deepcopy(grid)

    pos = sample_square(grid, full=True, num=9*9-init_num)
    for i in range(len(pos)):
        grid[pos[i][0]][pos[i][1]] = 0

    xy = [(i,j) for i in range(9) for j in range(9) if grid[i][j] > 0]
    num_full = len(xy)
    print("Sudoku Grid Ready. Num-full="+str(num_full))
    return grid, full_grid, xy


# Make board from scracth or from existing board. Taken and modified from stackexchange:
# https://codereview.stackexchange.com/questions/88849/sudoku-puzzle-generator
def make_board(m=3, diag=False):
    """Return a random filled m**2 x m**2 Sudoku board."""
    from ex4 import find_all_conflicts, sudoku_iscomplete

    n = m**2
    board = [[0 for _ in range(n)] for _ in range(n)]
    if len(find_all_conflicts(board)) > 0:
        return 0
    else:
        if sudoku_iscomplete(board):  # filled
            return board




    def local_search(c=0):
        "Recursively search for a solution starting at position c."
        i, j = divmod(c, n)
        i0, j0 = i - i % m, j - j % m  # Origin of mxm block
        numbers = list(range(1, n + 1))
        random.shuffle(numbers)

        if board[i][j] > 0:  # already filled!
            if c + 1 >= n ** 2 or local_search(c + 1):  # Here finished?
                return board
        else:
            for x in numbers:
                check_diag = True
                if i == j and diag: # check diagonal
                    check_diag = all(board[k][k] != x for k in range(n))
                if i + j == n-1 and diag:
                    check_diag = all(board[k][n-1-k] != x for k in range(n))

                if (check_diag and x not in board[i]       # diag, row
                    and all(row[j] != x for row in board)  # column
                    and all(x not in row[j0:j0+m]          # block
                            for row in board[i0:i])):
                    board[i][j] = x
                    if c + 1 >= n**2 or local_search(c + 1):  # Here finished?
                        return board
            else:  # no x matches !! executed after for loop !
                # No number is valid in this cell: backtrack and try again.
                board[i][j] = 0  # None
                return 0  # None

    return local_search()


# Display sudoku: 9*9 board with values at (x,y) coordiantes equal to val
def display_sudoku(board, size=[9,9], xy=[]):

    from ex4 import find_all_conflicts
    pygame.init()
    CELLSIZE = 40

    screen = pygame.display.set_mode((CELLSIZE*(size[1]+2), CELLSIZE*(size[0]+2)))
    font = pygame.font.Font(None, CELLSIZE)
    tinyfont = pygame.font.Font(None, int(CELLSIZE*0.45))

    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)
    BLUE = (0, 0, 255)

    screen.fill(WHITE)
    for i in range(size[0]+1):  # horizontal lines
        pygame.draw.line(screen, BLACK, (20, 20+CELLSIZE*(i+1)), (20+(size[1])*CELLSIZE,20+CELLSIZE*(i+1)), 1 + 4 * (i%3==0))
    for i in range(size[1]+1):  # vertical lines
        pygame.draw.line(screen, BLACK, (20 + CELLSIZE*i, 20+CELLSIZE), (20 + CELLSIZE*i, 20+(size[0]+1)*CELLSIZE), 1 + 4 * (i%3==0))

    conflicts = find_all_conflicts(board)
    for i in range(size[0]):  # draw filled numbers
        for j in range(size[1]):
            if board[i][j] > 0 or [i,j] in conflicts:

                if (i,j) in xy:  #  and j in y:  # init squares
                    text = font.render(str(board[i][j]), CELLSIZE, BLACK)  # get text from initialization
                elif [i,j] in conflicts:
                    if board[i][j] > 0:
                        text = font.render(str(board[i][j]), CELLSIZE, RED)  # conflict. Filled square
                    else:
                        text = font.render('?', CELLSIZE, RED)  # conflict. Empty square
                else:
                    text = font.render(str(board[i][j]), CELLSIZE, BLUE)  # get text from solution
                screen.blit(text, (CELLSIZE * (j + 0.8), CELLSIZE * (i + 1.65)))  # display

    for i in range(size[0]):  # draw x-ticks
        text = font.render(str(i+1), int(CELLSIZE*0.25), BLACK)  # get index
        screen.blit(text, (CELLSIZE * (0.05), CELLSIZE * (i + 1.65)))  # display
        screen.blit(text, (CELLSIZE * (i+ 0.9), CELLSIZE * 0.8))  # display

    pygame.display.flip()


# Sample a random square from all non-filled square
def sample_square(board, full=False, num=1):
    if full:
        pos = random.sample([(i, j) for i in range(9) for j in range(9) if board[i][j] > 0], num)  # [0:num]  # select random full square (for removal)
    else:  # here sample an empty square
        pos = random.sample([(i, j) for i in range(9) for j in range(9) if board[i][j] == 0], num)  # [0:num]  # select random empty square
    return pos

