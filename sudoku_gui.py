import solver
import pygame
import sys
from copy import deepcopy

DARK_BLUE = (30, 32, 40)
WHITE = (250, 250, 250)


class Puzzle:
    def __init__(self):
        self.puzzle_num = 0
        self.puzzles = [[[3, 0, 6, 5, 0, 8, 4, 0, 0],
                         [5, 2, 0, 0, 0, 0, 0, 0, 0],
                         [0, 8, 7, 0, 0, 0, 0, 3, 1],
                         [0, 0, 3, 0, 1, 0, 0, 8, 0],
                         [9, 0, 0, 8, 6, 3, 0, 0, 5],
                         [0, 5, 0, 0, 9, 0, 6, 0, 0],
                         [1, 3, 0, 0, 0, 0, 2, 5, 0],
                         [0, 0, 0, 0, 0, 0, 0, 7, 4],
                         [0, 0, 5, 2, 0, 6, 3, 0, 0]],

                        [[2, 0, 0, 3, 0, 0, 0, 0, 0],
                         [8, 0, 4, 0, 6, 2, 0, 0, 3],
                         [0, 1, 3, 8, 0, 0, 2, 0, 0],
                         [0, 0, 0, 0, 2, 0, 3, 9, 0],
                         [5, 0, 7, 0, 0, 0, 6, 2, 1],
                         [0, 3, 2, 0, 0, 6, 0, 0, 0],
                         [0, 2, 0, 0, 0, 9, 1, 4, 0],
                         [6, 0, 1, 2, 5, 0, 8, 0, 9],
                         [0, 0, 0, 0, 0, 1, 0, 0, 2]],

                        [[0, 2, 0, 0, 0, 0, 0, 0, 0],
                         [0, 0, 0, 6, 0, 0, 0, 0, 3],
                         [0, 7, 4, 0, 8, 0, 0, 0, 0],
                         [0, 0, 0, 0, 0, 3, 0, 0, 2],
                         [0, 8, 0, 0, 4, 0, 0, 1, 0],
                         [6, 0, 0, 5, 0, 0, 0, 0, 0],
                         [0, 0, 0, 0, 1, 0, 7, 8, 0],
                         [5, 0, 0, 0, 0, 9, 0, 0, 0],
                         [0, 0, 0, 0, 0, 0, 0, 4, 0]],

                        [[0, 0, 0, 6, 0, 0, 4, 0, 0],
                         [7, 0, 0, 0, 0, 3, 6, 0, 0],
                         [0, 0, 0, 0, 9, 1, 0, 8, 0],
                         [0, 0, 0, 0, 0, 0, 0, 0, 0],
                         [0, 5, 0, 1, 8, 0, 0, 0, 3],
                         [0, 0, 0, 3, 0, 6, 0, 4, 5],
                         [0, 4, 0, 2, 0, 0, 0, 6, 0],
                         [9, 0, 3, 0, 0, 0, 0, 0, 0],
                         [0, 2, 0, 0, 0, 0, 1, 0, 0]],
                        ]

    def new(self):
        """Move to the next puzzle in the list."""
        self.puzzle_num += 1
        if self.puzzle_num == 4:
            self.puzzle_num = 0
        return deepcopy(self.puzzles[self.puzzle_num])

    def get(self):
        """Return the current puzzle."""
        return deepcopy(self.puzzles[self.puzzle_num])


class SudokuGUI:
    clock = pygame.time.Clock()

    # Colors
    WHITE = (250, 250, 250)
    LIGHT_GRAY = (150, 150, 150)
    GRAY = (100, 100, 100)
    LIGHT_BLUE = (66, 112, 173)
    BLUE = (43, 94, 161)
    DARK_BLUE = (30, 32, 40)

    # Speed colors
    RED = (148, 55, 47)
    ORANGE = (199, 130, 66)
    YELLOW = (207, 186, 68)
    YELLOW_GREEN = (200, 209, 67)
    GREEN = (81, 138, 45)

    def __init__(self, board: list, display: pygame.display):
        self.speed = 180  # values are 30, 60, 180, 300, -1
        self.puzzle = deepcopy(board)
        self.puzzle_copy = deepcopy(board)
        self.display = display

    def draw_empty_board(self) -> None:
        """Draw an empty sudoku board."""
        font = pygame.font.SysFont('freesansbold.ttf', 80)
        text_surface = font.render('Sudoku Solver', True, self.WHITE)
        self.display.blit(text_surface, (45, 65))

        square_size = (55, 55)
        for grid_x in range(0, 400, 185):
            for grid_y in range(0, 400, 185):
                for x in range(0, 121, 60):
                    for y in range(0, 121, 60):
                        pygame.draw.rect(self.display, self.WHITE, ((45 + x + grid_x, 120 + y + grid_y), square_size))

    def draw_numbers(self, color: tuple, use_copy=False) -> None:
        """Draw the numbers in the current sudoku board."""
        font = pygame.font.SysFont('freesansbold.ttf', 40)
        for grid_y in range(3):
            for grid_x in range(3):
                for row in range(3):
                    for col in range(3):
                        if use_copy:
                            num = self.puzzle_copy[row + (3 * grid_y)][col + (3 * grid_x)]
                        else:
                            num = self.puzzle[row + (3 * grid_y)][col + (3 * grid_x)]
                        if num:
                            num_surface = font.render(str(num), True, color)
                            self.display.blit(num_surface, (65 + (60 * (col + (3 * grid_x))) + (5 * grid_x),
                                                            135 + (60 * (row + (3 * grid_y))) + (5 * grid_y)))

    def draw_buttons(self) -> None:
        """Draw the buttons."""
        mouse_pos = pygame.mouse.get_pos()
        button_font = pygame.font.SysFont('freesansbold.ttf', 48)

        for i in range(3):
            if 730 < mouse_pos[0] < 970 and 120 + (110 * i) < mouse_pos[1] < 190 + (110 * i):
                pygame.draw.rect(self.display, self.LIGHT_BLUE, ((725, 115 + (110 * i)), (250, 80)))
            pygame.draw.rect(self.display, self.WHITE, ((730, 120 + (110 * i)), (240, 70)))

        self.display.blit(button_font.render('NEW PUZZLE', True, self.DARK_BLUE), (742, 142))
        self.display.blit(button_font.render('SOLVE', True, self.DARK_BLUE), (796, 252))
        self.display.blit(button_font.render('QUICK SOLVE', True, self.DARK_BLUE), (738, 361))

        self._draw_speed_button(mouse_pos)

    def _draw_speed_button(self, mouse_pos: tuple) -> None:
        """Helper function to draw the speed buttons."""
        colors = [(30, self.RED), (60, self.ORANGE), (180, self.YELLOW), (300, self.YELLOW_GREEN), (-1, self.GREEN)]
        button_font = pygame.font.SysFont('freesansbold.ttf', 48)

        for i in range(5):
            if 688 + (65 * i) < mouse_pos[0] <= 754 + (65 * i) and 550 < mouse_pos[1] < 605:
                pygame.draw.rect(self.display, self.WHITE, ((689, 545), (65 * (i + 1), 65)))
        for i in range(5):
            if (self.speed == -1) or (self.speed >= colors[i][0] != -1):
                pygame.draw.rect(self.display, colors[i][1], ((694 + (i * 65), 550), (55, 55)))
            else:
                pygame.draw.rect(self.display, self.GRAY, ((694 + (i * 65), 550), (55, 55)))

        speed_text_surface = button_font.render('SPEED', True, self.WHITE)
        self.display.blit(speed_text_surface, (796, 500))

    def new_puzzle(self, new: list):
        """Change the current puzzle to a new one."""
        self.puzzle = deepcopy(new)
        self.puzzle_copy = deepcopy(new)

    def quick_solve(self, use_copy=False):
        """Solve the puzzle without drawing the steps."""
        button_font = pygame.font.SysFont('freesansbold.ttf', 48)
        r = pygame.draw.rect(self.display, self.WHITE, ((730, 340), (240, 70)))
        self.display.blit(button_font.render('SOLVING...', True, DARK_BLUE), (768, 360))
        pygame.display.update(r)
        
        if use_copy:
            solver.solve(self.puzzle_copy)
            self.puzzle = deepcopy(self.puzzle_copy)
        else:
            solver.solve(self.puzzle)

    def new_speed(self):
        """Change the speed when the speed buttons are clicked."""
        mouse_pos = pygame.mouse.get_pos()
        if 688 < mouse_pos[0] < 1019 and 550 < mouse_pos[1] < 605:
            self.speed = 30
        if 753 < mouse_pos[0] < 1019 and 550 < mouse_pos[1] < 605:
            self.speed = 60
        if 823 < mouse_pos[0] < 1019 and 550 < mouse_pos[1] < 605:
            self.speed = 180
        if 888 < mouse_pos[0] < 1019 and 550 < mouse_pos[1] < 605:
            self.speed = 300
        if 953 < mouse_pos[0] < 1019 and 550 < mouse_pos[1] < 605:
            self.speed = -1

    def solve(self) -> bool:
        """Solve the sudoku board recursively using a backtracking algorithm
        and shows the steps visually."""

        coordinates = solver.find_empty(self.puzzle)
        if not coordinates:
            return True

        row, col = coordinates
        grid_x = col // 3
        grid_y = row // 3
        square_size = (55, 55)

        for i in range(1, 10):
            self.clock.tick(self.speed)
            self.display.fill(DARK_BLUE)
            self.draw_empty_board()
            self.draw_numbers(DARK_BLUE)
            self.draw_buttons()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                    
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    if 688 < mouse_pos[0] < 1019 and 550 < mouse_pos[1] < 605:
                        self.new_speed()
                        
                    if 730 < mouse_pos[0] < 970 and 340 < mouse_pos[1] < 410:
                        self.quick_solve(use_copy=True)
                        return True

            if solver.is_valid(self.puzzle, row, col, i):
                self.puzzle[row][col] = i
                self.draw_empty_board()
                pygame.draw.rect(self.display, self.GREEN, ((45 + (col * 60) + (grid_x * 5),
                                                             120 + (row * 60) + (grid_y * 5)), square_size))
                self.draw_numbers(self.GREEN)
                self.draw_numbers(self.DARK_BLUE, use_copy=True)
                pygame.display.update()

                if self.solve():
                    return True
                
            self.puzzle[row][col] = 0
            self.draw_empty_board()
            pygame.draw.rect(self.display, self.RED, ((45 + (col * 60) + (grid_x * 5),
                                                       120 + (row * 60) + (grid_y * 5)), square_size))
            self.draw_numbers(self.GREEN)
            self.draw_numbers(self.DARK_BLUE, use_copy=True)
            pygame.display.update()

        return False


def main():
    pygame.init()
    puzzle = Puzzle()
    display = pygame.display.set_mode((1080, 720))
    sudoku = SudokuGUI(puzzle.get(), display)
    running = True

    while running:
        display.fill(DARK_BLUE)
        sudoku.draw_empty_board()
        sudoku.draw_numbers(DARK_BLUE)
        mouse_pos = pygame.mouse.get_pos()
        sudoku.draw_buttons()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if 730 < mouse_pos[0] < 970 and 120 < mouse_pos[1] < 190:
                    new = puzzle.new()
                    sudoku.new_puzzle(new)

                if 730 < mouse_pos[0] < 970 and 340 < mouse_pos[1] < 410:
                    sudoku.quick_solve()

                if 730 < mouse_pos[0] < 970 and 230 < mouse_pos[1] < 300:
                    sudoku.solve()

                if 688 < mouse_pos[0] < 1019 and 550 < mouse_pos[1] < 605:
                    sudoku.new_speed()
        pygame.display.update()


main()
