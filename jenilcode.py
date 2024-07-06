import random
import tkinter as tk
from tkinter import messagebox

class SudokuBoard:
    def __init__(self):
        self.board = [[0 for _ in range(9)] for _ in range(9)]

    def is_valid_move(self, row, col, num):
        # Check row
        if num in self.board[row]:
            return False
        # Check column
        if num in [self.board[i][col] for i in range(9)]:
            return False
        # Check 3x3 box
        box_row, box_col = 3 * (row // 3), 3 * (col // 3)
        for i in range(box_row, box_row + 3):
            for j in range(box_col, box_col + 3):
                if self.board[i][j] == num:
                    return False
        return True

    def find_empty(self):
        for i in range(9):
            for j in range(9):
                if self.board[i][j] == 0:
                    return i, j
        return None

    def heuristic(self):
        return sum(row.count(0) for row in self.board)

class SudokuSolver:
    def __init__(self, board):
        self.board = board

    def solve(self):
        return self._a_star()

    def _a_star(self):
        start_node = (self.board, 0)
        open_list = [start_node]
        closed_set = set()

        while open_list:
            current_node = min(open_list, key=lambda x: x[1] + x[0].heuristic())
            open_list.remove(current_node)

            if current_node[0].heuristic() == 0:
                return current_node[0]

            closed_set.add(str(current_node[0].board))

            for neighbor in self._get_neighbors(current_node[0]):
                if str(neighbor.board) not in closed_set:
                    open_list.append((neighbor, current_node[1] + 1))

        return None

    def _get_neighbors(self, board):
        neighbors = []
        empty = board.find_empty()
        if not empty:
            return neighbors

        row, col = empty
        for num in range(1, 10):
            if board.is_valid_move(row, col, num):
                new_board = SudokuBoard()
                new_board.board = [row[:] for row in board.board]
                new_board.board[row][col] = num
                neighbors.append(new_board)

        return neighbors

def generate_sudoku(difficulty):
    board = SudokuBoard()
    solver = SudokuSolver(board)
    solved_board = solver.solve()

    if solved_board:
        cells_to_remove = difficulty * 9
        while cells_to_remove > 0:
            row, col = random.randint(0, 8), random.randint(0, 8)
            if solved_board.board[row][col] != 0:
                solved_board.board[row][col] = 0
                cells_to_remove -= 1

    return solved_board

class SudokuGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("Sudoku")
        self.board = generate_sudoku(4)  # Adjust difficulty (1-5)
        self.cells = {}
        self.create_board()
        self.create_buttons()

    def create_board(self):
        for i in range(9):
            for j in range(9):
                cell_value = self.board.board[i][j]
                cell = tk.Entry(self.master, width=2, font=('Arial', 18), justify='center')
                cell.grid(row=i, column=j, padx=1, pady=1)
                
                if cell_value != 0:
                    cell.insert(0, str(cell_value))
                    cell.config(state='readonly')
                
                self.cells[(i, j)] = cell

                if i % 3 == 2 and i < 8:
                    separator = tk.Frame(self.master, height=2, bd=1, relief=tk.SUNKEN)
                    separator.grid(row=i+1, column=0, columnspan=9, sticky="ew")

                if j % 3 == 2 and j < 8:
                    separator = tk.Frame(self.master, width=2, bd=1, relief=tk.SUNKEN)
                    separator.grid(row=0, column=j+1, rowspan=9, sticky="ns")

    def create_buttons(self):
        solve_button = tk.Button(self.master, text="Solve", command=self.solve_sudoku)
        solve_button.grid(row=9, column=0, columnspan=3, pady=10)

        check_button = tk.Button(self.master, text="Check", command=self.check_solution)
        check_button.grid(row=9, column=3, columnspan=3, pady=10)

        new_game_button = tk.Button(self.master, text="New Game", command=self.new_game)
        new_game_button.grid(row=9, column=6, columnspan=3, pady=10)

    def solve_sudoku(self):
        solver = SudokuSolver(self.board)
        solution = solver.solve()
        if solution:
            for i in range(9):
                for j in range(9):
                    self.cells[(i, j)].config(state='normal')
                    self.cells[(i, j)].delete(0, tk.END)
                    self.cells[(i, j)].insert(0, str(solution.board[i][j]))
                    self.cells[(i, j)].config(state='readonly')
        else:
            messagebox.showinfo("No Solution", "This Sudoku puzzle has no solution.")

    def check_solution(self):
        for i in range(9):
            for j in range(9):
                value = self.cells[(i, j)].get()
                if value == "":
                    messagebox.showinfo("Incomplete", "Please fill in all cells before checking.")
                    return
                self.board.board[i][j] = int(value)

        solver = SudokuSolver(self.board)
        if solver.solve():
            messagebox.showinfo("Correct", "Your solution is correct!")
        else:
            messagebox.showinfo("Incorrect", "Your solution is incorrect. Please try again.")

    def new_game(self):
        self.board = generate_sudoku(4)  # Adjust difficulty (1-5)
        for i in range(9):
            for j in range(9):
                cell_value = self.board.board[i][j]
                self.cells[(i, j)].config(state='normal')
                self.cells[(i, j)].delete(0, tk.END)
                if cell_value != 0:
                    self.cells[(i, j)].insert(0, str(cell_value))
                    self.cells[(i, j)].config(state='readonly')

if __name__ == "__main__":
    root = tk.Tk()
    game = SudokuGUI(root)
    root.mainloop()