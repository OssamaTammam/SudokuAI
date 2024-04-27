import pygame
import numpy as np

from CSP import CSP


class GUI:
    def __init__(self):
        pygame.init()
        self.WIDTH = 500
        self.HEIGHT = 500
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("Sudoku Solver")
        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)
        self.GRAY = (128, 128, 128)
        self.font = pygame.font.Font(None, 40)
        self.cell_size = self.WIDTH // 9
        self.mode = 1

        # self.grid = np.zeros((9, 9), dtype=int)
        self.grid = np.array(
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

    def draw_grid(self):
        for i in range(10):
            if i % 3 == 0:
                thickness = 5
            else:
                thickness = 1
            pygame.draw.line(
                self.screen,
                self.BLACK,
                (i * self.cell_size, 0),
                (i * self.cell_size, self.HEIGHT),
                thickness,
            )
            pygame.draw.line(
                self.screen,
                self.BLACK,
                (0, i * self.cell_size),
                (self.WIDTH, i * self.cell_size),
                thickness,
            )

    def draw_number(
        self,
    ):
        for i in range(9):
            for j in range(9):
                if self.grid[i][j] != 0:
                    number = self.font.render(str(self.grid[i][j]), True, self.BLACK)
                    self.screen.blit(
                        number, (j * self.cell_size + 20, i * self.cell_size + 20)
                    )

    def solve_sudoku(self):
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

        for i in range(9):
            for j in range(9):
                if self.grid[i][j] != 0:
                    csp.domains[(i, j)] = [self.grid[i][j]]

        solution = csp.solve()
        if solution:
            for i in range(9):
                for j in range(9):
                    self.grid[i][j] = solution[(i, j)]

    def main(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.solve_sudoku()

            self.screen.fill(self.WHITE)
            self.draw_grid()
            self.draw_number()
            pygame.display.flip()
        pygame.quit()


if __name__ == "__main__":
    gui = GUI()
    gui.main()
