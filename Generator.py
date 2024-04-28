import random
from CSP import CSP
import numpy as np


class SudokuGenerator:
    def __init__(self):
        self.solved_grid = np.array(
            [
                [5, 3, 0, 0, 7, 0, 0, 0, 0],
                [6, 0, 0, 1, 9, 5, 0, 0, 0],
                [0, 9, 8, 0, 0, 0, 0, 6, 0],
                [8, 0, 0, 0, 6, 0, 0, 0, 3],
                [4, 0, 0, 8, 0, 3, 0, 0, 1],
                [7, 0, 0, 0, 2, 0, 0, 0, 6],
                [0, 6, 0, 0, 0, 0, 2, 8, 0],
                [0, 0, 0, 4, 1, 9, 0, 0, 5],
                [0, 0, 0, 0, 8, 0, 0, 7, 9],
            ]
        )

    def generate_complete_puzzle(self):
        csp = CSP(
            variables=[(i, j) for i in range(9) for j in range(9)],
            domains={(i, j): list(range(1, 10)) for i in range(9) for j in range(9)},
            constraints=[
                ((var_i_row, var_i_col), (var_j_row, var_j_col))
                for var_i_row in range(9)
                for var_i_col in range(9)
                for var_j_row in range(9)
                for var_j_col in range(9)
                if (var_i_row != var_j_row or var_i_col != var_j_col)
                and (
                    var_i_row == var_j_row
                    or var_i_col == var_j_col
                    or (
                        var_i_row // 3 == var_j_row // 3
                        and var_i_col // 3 == var_j_col // 3
                    )
                )
            ],
        )

        # Solve the puzzle
        solution = csp.solve()

        if solution:
            for i in range(9):
                for j in range(9):
                    self.solved_grid[i][j] = solution[(i, j)]

    def remove_elements(self, num_remove):
        if self.solved_grid is None:
            print("Generate a complete puzzle first.")
            return

        # Randomly remove elements while ensuring puzzle remains solvable
        for _ in range(num_remove):
            row, col = random.randint(0, 8), random.randint(0, 8)
            if self.solved_grid[row, col] != 0:  # Ensure the cell is not already empty
                original_value = self.solved_grid[row, col]
                self.solved_grid[row, col] = 0  # Remove the value

    def generate_puzzle(self):
        self.generate_complete_puzzle()
        no_elements = random.randint(17, 30)
        self.remove_elements(81 - no_elements)
        return self.solved_grid
