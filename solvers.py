
#Functions used to solve the sudoku puzzle

def find_empty_location(grid):
    for row in range(9):
        for col in range(9):
            if grid[row][col] == 0:
                return (row, col)
    return None

def is_valid(grid, row, col, num):
    #Checks whether or not the num is in the current row
    if num in grid[row]:
        return False

    #Checks whether or not the num is in the current column
    if num in [grid[i][col] for i in range(9)]:
        return False

    #Checks whether or not the num is in the current 3x3 grid
    start_row, start_col = 3 * (row // 3), 3 * (col // 3)
    for i in range(start_row, start_row + 3):
        for j in range(start_col, start_col + 3):
            if grid[i][j] == num:
                return False

    return True


def solve_sudoku(grid):
    empty_location = find_empty_location(grid)
    #The puzzle is solved!
    if not empty_location:
        return True

    row, col = empty_location

    for num in range(1, 10):
        if is_valid(grid, row, col, num):
            grid[row][col] = num

            #RECURSION WOOHOO!
            if solve_sudoku(grid):
                return True

            #Reseting the cell for backtracking: thank God for sudoku algorithms and wikipedia because I literally couldn't have figured this stuff out on my own
            grid[row][col] = 0

    return False
