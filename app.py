
import os
import secrets

from flask import Flask, flash, redirect, render_template, request
from solvers import solve_sudoku


#Configure application
app = Flask(__name__)

#Create key for flash messages
app.secret_key = secrets.token_hex(16)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/learn')
def learn():
    return render_template('learn.html')

@app.route('/resources')
def resources():
    return render_template('resources.html')

@app.route('/solve', methods=['POST'])
def solve():
    #Creates a 2d array of 0s, which will be used to store the sudoku table
    sudoku_grid = [[0 for _ in range(9)] for _ in range(9)]
    #Tracking user inputs to highlight solved numbers (when the puzzle is solved)
    user_entries = [[None for _ in range(9)] for _ in range(9)]
    has_error = False

    for row in range(9):
        for col in range(9):
            #Getting the value of each cell, 0 by default, then appending it if it is a valid integer
            cell_value = request.form.get(f'cell-{row}-{col}', '').strip()
            if cell_value.isdigit() and 0 <= int(cell_value) <= 9:
                sudoku_grid[row][col] = int(cell_value)
                user_entries[row][col] = int(cell_value)
            #Defaults to 0 as the cell value in the case that the user does not enter anything, or enters 0
            elif cell_value == '' or cell_value == 0:
                sudoku_grid[row][col] = 0
                user_entries[row][col] = None
            #Throws an error (flash message) if the user input is invalid
            else:
                flash(f'Invalid at row {row+1}, column {col+1}. Please enter a valid, single digit number.', 'error')
                has_error = True
                break
        if has_error:
            break

    if has_error:
        return redirect('/')

    #Checking whether or not a grid is empty or contains zeros, which are considered to be empty
    if all(all(cell == 0 for cell in row) for row in sudoku_grid):
        flash('The Sudoku Table is completely empty. Please enter at least one valid, single digit number.', 'error')
        return redirect('/')

    #If the table passed the checks, it is now validated and can be solved.
    if solve_sudoku(sudoku_grid):
        flash('Table has been solved!', 'success')
    else:
        flash('Unable to solve the Sudoku Puzzle; please double check your inputs for each cell and try again.', 'error')

    #Render the updated table
    return render_template('index.html', sudoku_grid=sudoku_grid, user_entries=user_entries)

if __name__ == '__main__':
    app.run(debug=False)
