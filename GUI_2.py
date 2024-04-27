import pygame
import numpy as np
from CSP import CSP
import time


class GUI:
    def __init__(self):
        pygame.init()
        self.WIDTH = 500
        self.HEIGHT = 500
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT + 200))
        pygame.display.set_caption("Sudoku Solver")
        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)
        self.GRAY = (128, 128, 128)
        self.font = pygame.font.Font(None, 40)
        self.cell_size = self.WIDTH // 9
        self.mode = 1
        self.selected_row = None
        self.selected_col = None
        self.solved = False
        self.board_unsolvable = False

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

        # Add mode buttons
        button_width = 100
        button_height = 30
        self.mode1_button = pygame.Rect(
            (self.WIDTH - button_width) // 2,
            self.HEIGHT + 10,
            button_width,
            button_height,
        )
        self.mode2_button = pygame.Rect(
            (self.WIDTH - button_width) // 2,
            self.HEIGHT + 50,
            button_width,
            button_height,
        )

        self.mode3_button = pygame.Rect(
            (self.WIDTH - button_width) // 2,
            self.HEIGHT + 90,
            button_width,
            button_height,
        )

        self.mode_buttons_color = self.GRAY
        self.mode_buttons_text_color = self.BLACK
        self.mode_buttons_font = pygame.font.Font(None, 24)

    def draw_mode_buttons(self):
        # Mode 1 button
        pygame.draw.rect(self.screen, self.mode_buttons_color, self.mode1_button)
        mode1_text = self.mode_buttons_font.render(
            "Mode 1", True, self.mode_buttons_text_color
        )
        mode1_text_rect = mode1_text.get_rect(center=self.mode1_button.center)
        self.screen.blit(mode1_text, mode1_text_rect)

        # Mode 2 button
        pygame.draw.rect(self.screen, self.mode_buttons_color, self.mode2_button)
        mode2_text = self.mode_buttons_font.render(
            "Mode 2", True, self.mode_buttons_text_color
        )
        mode2_text_rect = mode2_text.get_rect(center=self.mode2_button.center)
        self.screen.blit(mode2_text, mode2_text_rect)

        pygame.draw.rect(self.screen, self.mode_buttons_color, self.mode3_button)
        mode3_text = self.mode_buttons_font.render(
            "Mode 3", True, self.mode_buttons_text_color
        )
        mode3_text_rect = mode3_text.get_rect(center=self.mode3_button.center)
        self.screen.blit(mode3_text, mode3_text_rect)

    def handle_mode_buttons_click(self, pos):
        if self.mode1_button.collidepoint(pos):
            self.solved = False
            self.mode = 1
            print("Mode 1 selected")
        elif self.mode2_button.collidepoint(pos):
            self.solved = False
            self.mode = 2
            self.grid = np.zeros((9, 9), dtype=int)
            print("Mode 2 selected")
        elif self.mode3_button.collidepoint(pos):
            self.solved = False
            self.mode = 3
            self.grid = np.zeros((9, 9), dtype=int)
            print("Mode 3 selected")

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

    def draw_number(self):
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

        start_time = time.time()
        solution = csp.solve()
        end_time = time.time()

        if solution:
            for i in range(9):
                for j in range(9):
                    self.grid[i][j] = solution[(i, j)]
        else:
            self.board_unsolvable = True

        csp.print_arc_trees()
        print("Run Time: ", end_time - start_time, " Seconds")

    def fill_grid(self, row, col, value):
        if 0 <= row < 9 and 0 <= col < 9 and 0 <= value <= 9:
            self.grid[row][col] = value

    def check_validity(self, row, col):
        for x in range(9):
            if self.grid[row][col] == self.grid[row][x] and x != col:
                self.grid[row][col] = 0
                return False
            if self.grid[row][col] == self.grid[x][col] and x != row:
                self.grid[row][col] = 0
                return False
            box_x = col // 3
            box_y = row // 3
            for m in range(box_y * 3, box_y * 3 + 3):
                for n in range(box_x * 3, box_x * 3 + 3):
                    if self.grid[row][col] == self.grid[m][n] and (m, n) != (row, col):
                        self.grid[row][col] = 0
                        return False
        return True

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if (
                    self.mode1_button.collidepoint(mouse_pos)
                    or self.mode2_button.collidepoint(mouse_pos)
                    or self.mode3_button.collidepoint(mouse_pos)
                ):
                    self.handle_mode_buttons_click(mouse_pos)
                else:
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    self.selected_row = mouse_y // self.cell_size
                    self.selected_col = mouse_x // self.cell_size
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.solved = True
                    self.solve_sudoku()
                elif (
                    event.key
                    in [
                        pygame.K_0,
                        pygame.K_1,
                        pygame.K_2,
                        pygame.K_3,
                        pygame.K_4,
                        pygame.K_5,
                        pygame.K_6,
                        pygame.K_7,
                        pygame.K_8,
                        pygame.K_9,
                    ]
                    and self.mode == 2
                    and not self.solved
                ):
                    if self.selected_row is not None and self.selected_col is not None:
                        self.fill_grid(
                            self.selected_row, self.selected_col, int(event.unicode)
                        )
                elif (
                    (
                        event.key
                        in [
                            pygame.K_0,
                            pygame.K_1,
                            pygame.K_2,
                            pygame.K_3,
                            pygame.K_4,
                            pygame.K_5,
                            pygame.K_6,
                            pygame.K_7,
                            pygame.K_8,
                            pygame.K_9,
                        ]
                    )
                    and self.mode == 3
                    and not self.solved
                ):
                    if self.selected_row is not None and self.selected_col is not None:
                        self.fill_grid(
                            self.selected_row, self.selected_col, int(event.unicode)
                        )
                        if self.check_validity(self.selected_row, self.selected_col):
                            print("Entry is valid!")
                        else:
                            print("Entry violates Sudoku rules!")
        pygame.display.flip()

    def main(self):
        clock = pygame.time.Clock()
        running = True
        while running:
            self.screen.fill(self.WHITE)
            self.draw_grid()
            self.draw_number()
            self.draw_mode_buttons()
            if self.board_unsolvable:
                text = self.font.render("Board can't be solved", True, self.BLACK)
                text_rect = text.get_rect(center=(self.WIDTH // 2, self.HEIGHT + 80))
                self.screen.blit(text, text_rect)
            self.handle_events()
            clock.tick(30)


if __name__ == "__main__":
    gui = GUI()
    gui.main()
