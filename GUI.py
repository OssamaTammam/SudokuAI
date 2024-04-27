import pygame  # Importing Pygame library for building GUI applications
import numpy as np  # Importing NumPy library for numerical operations
from CSP import (
    CSP,
)  # Importing the CSP module for solving Constraint Satisfaction Problems
import time  # Importing time module for time-related functions


class GUI:
    def __init__(self):
        pygame.init()  # Initializing Pygame
        self.WIDTH = 500  # Setting the width of the window
        self.HEIGHT = 500  # Setting the height of the window
        self.screen = pygame.display.set_mode(
            (self.WIDTH, self.HEIGHT + 100)
        )  # Creating the Pygame display window
        pygame.display.set_caption("Sudoku Solver")  # Setting the title of the window
        self.WHITE = (255, 255, 255)  # Defining colors
        self.BLACK = (0, 0, 0)
        self.GRAY = (128, 128, 128)
        self.font = pygame.font.Font(None, 40)  # Defining font for text rendering
        self.cell_size = self.WIDTH // 9  # Calculating cell size for Sudoku grid
        self.mode = 1  # Initializing mode (1 or 2)
        self.selected_row = None  # Initializing selected row and column
        self.selected_col = None
        self.solved = False  # Flag to indicate if Sudoku puzzle is solved
        self.board_unsolvable = False  # Flag to indicate if the board is unsolvable

        # Initial Sudoku puzzle grid
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
        # Define mode buttons' rectangles
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
        self.mode_buttons_color = self.GRAY  # Color for mode buttons
        self.mode_buttons_text_color = self.BLACK  # Text color for mode buttons
        self.mode_buttons_font = pygame.font.Font(None, 24)  # Font for mode buttons

    def draw_mode_buttons(self):
        # Draw mode buttons
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

    def handle_mode_buttons_click(self, pos):
        # Handle mode buttons click event
        if self.mode1_button.collidepoint(pos):
            self.mode = 1
            print("Mode 1 selected")
        elif self.mode2_button.collidepoint(pos) and self.mode == 1:
            self.solved = False
            self.mode = 2
            self.grid = np.zeros((9, 9), dtype=int)
            print("Mode 2 selected")

    def draw_grid(self):
        # Draw Sudoku grid
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
        # Draw numbers on Sudoku grid
        for i in range(9):
            for j in range(9):
                if self.grid[i][j] != 0:
                    number = self.font.render(str(self.grid[i][j]), True, self.BLACK)
                    self.screen.blit(
                        number, (j * self.cell_size + 20, i * self.cell_size + 20)
                    )

    def solve_sudoku(self):
        # Solve Sudoku puzzle using CSP solver
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

        csp.print_arc_trees()  # Print arc trees for debugging
        print("Time Took: ", (end_time - start_time), " Seconds")

    def fill_grid(self, row, col, value):
        # Fill Sudoku grid with a number
        if 0 <= row < 9 and 0 <= col < 9 and 0 <= value <= 9:
            self.grid[row][col] = value

    def handle_events(self):
        # Handle Pygame events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if self.mode1_button.collidepoint(
                    mouse_pos
                ) or self.mode2_button.collidepoint(mouse_pos):
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
        pygame.display.flip()

    def main(self):
        # Main loop of the GUI
        clock = pygame.time.Clock()
        running = True
        while running:
            self.screen.fill(self.WHITE)  # Fill the screen with white color
            self.draw_grid()  # Draw Sudoku grid
            self.draw_number()  # Draw numbers on the grid
            self.draw_mode_buttons()  # Draw mode buttons
            if self.board_unsolvable:
                text = self.font.render("Board can't be solved", True, self.BLACK)
                text_rect = text.get_rect(center=(self.WIDTH // 2, self.HEIGHT + 80))
                self.screen.blit(text, text_rect)
            self.handle_events()  # Handle Pygame events
            clock.tick(30)  # Cap the frame rate at 30 FPS


if __name__ == "__main__":
    gui = GUI()  # Create an instance of the GUI class
    gui.main()  # Call the main method to start the GUI application
