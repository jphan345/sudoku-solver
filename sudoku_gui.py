import solver
import pygame
import sys
import copy

clock = pygame.time.Clock()
SPEED = 120

WHITE = (250, 250, 250)
DARK_BLUE = (30, 32, 40)
BLUE = (43, 94, 161)
LIGHT_BLUE = (66, 112, 173)
GRAY = (100, 100, 100)
LIGHT_GRAY = (150, 150, 150)
RED = (148, 55, 47)
ORANGE = (199, 130, 66)
YELLOW = (207, 186, 68)
YELLOW_GREEN = (200, 209, 67)
GREEN = (81, 138, 45)

speed_1_col = True
speed_2_col = True
speed_3_col = True
speed_4_col = False
speed_5_col = False

puzzle_num = 0
puzzle = [[3, 0, 6, 5, 0, 8, 4, 0, 0],
          [5, 2, 0, 0, 0, 0, 0, 0, 0],
          [0, 8, 7, 0, 0, 0, 0, 3, 1],
          [0, 0, 3, 0, 1, 0, 0, 8, 0],
          [9, 0, 0, 8, 6, 3, 0, 0, 5],
          [0, 5, 0, 0, 9, 0, 6, 0, 0],
          [1, 3, 0, 0, 0, 0, 2, 5, 0],
          [0, 0, 0, 0, 0, 0, 0, 7, 4],
          [0, 0, 5, 2, 0, 6, 3, 0, 0]]
puzzle_copy = copy.deepcopy(puzzle)


def draw_empty_board(display: pygame.display) -> None:
    font = pygame.font.SysFont('freesansbold.ttf', 80)
    text_surface = font.render('Sudoku Solver', True, WHITE)
    display.blit(text_surface, (45, 65))

    square_size = (55, 55)
    for grid_x in range(0, 400, 185):
        for grid_y in range(0, 400, 185):
            for x in range(0, 121, 60):
                for y in range(0, 121, 60):
                    pygame.draw.rect(display, WHITE, ((45 + x + grid_x, 120 + y + grid_y), square_size))


def draw_numbers(display: pygame.display, board: list, color: tuple) -> None:
    font = pygame.font.SysFont('freesansbold.ttf', 40)
    for grid_y in range(3):
        for grid_x in range(3):
            for row in range(3):
                for col in range(3):
                    num = board[row + (3 * grid_y)][col + (3 * grid_x)]
                    if num:
                        num_surface = font.render(str(num), True, color)
                        display.blit(num_surface, (65 + (60 * (col + (3 * grid_x))) + (5 * grid_x),
                                                   135 + (60 * (row + (3 * grid_y))) + (5 * grid_y)))


def solve_visual(board: list) -> bool:
    """Solve the sudoku board recursively using a backtracking algorithm.
    Rewritten to work for visualizing."""

    global speed_2_col
    global speed_3_col
    global speed_4_col
    global speed_5_col
    global SPEED
    global puzzle

    coordinates = solver.find_empty(board)
    if not coordinates:
        return True

    row, col = coordinates
    grid_x = col // 3
    grid_y = row // 3
    square_size = (55, 55)

    for i in range(1, 10):
        clock.tick(SPEED)

        display = pygame.display.set_mode((1080, 720))
        display.fill(DARK_BLUE)

        draw_empty_board(display)
        draw_numbers(display, board, DARK_BLUE)
        draw_buttons(display, pygame.mouse.get_pos())

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()

                # Pressed one of the speed options
                if 688 < mouse_pos[0] < 1019 and 550 < mouse_pos[1] < 605:
                    speed_2_col = False
                    speed_3_col = False
                    speed_4_col = False
                    speed_5_col = False
                    SPEED = 30
                if 753 < mouse_pos[0] < 1019 and 550 < mouse_pos[1] < 605:
                    speed_2_col = True
                    SPEED = 60
                if 823 < mouse_pos[0] < 1019 and 550 < mouse_pos[1] < 605:
                    speed_3_col = True
                    SPEED = 120
                if 888 < mouse_pos[0] < 1019 and 550 < mouse_pos[1] < 605:
                    speed_4_col = True
                    SPEED = 240
                if 953 < mouse_pos[0] < 1019 and 550 < mouse_pos[1] < 605:
                    speed_5_col = True
                    SPEED = -1

                # Pressed the 'SOLVE INSTANTLY' button
                if 730 < mouse_pos[0] < 970 and 340 < mouse_pos[1] < 410:
                    button_font = pygame.font.SysFont('freesansbold.ttf', 48)
                    r = pygame.draw.rect(display, WHITE, ((730, 340), (240, 70)))
                    display.blit(button_font.render('SOLVING...', True, DARK_BLUE), (768, 360))
                    pygame.display.update(r)

                    solver.solve(puzzle_copy)
                    puzzle = puzzle_copy
                    draw_empty_board(display)
                    draw_numbers(display, puzzle_copy, DARK_BLUE)
                    pygame.display.update()
                    return True

        if solver.is_valid(board, row, col, i):
            board[row][col] = i
            draw_empty_board(display)
            pygame.draw.rect(display, GREEN, ((45 + (col * 60) + (grid_x * 5), 120 + (row * 60) + (grid_y * 5)),
                                              square_size))

            draw_numbers(display, board, GREEN)
            draw_numbers(display, puzzle_copy, DARK_BLUE)
            pygame.display.update()

            if solve_visual(board):
                return True

        board[row][col] = 0
        draw_empty_board(display)
        pygame.draw.rect(display, RED, ((45 + (col * 60) + (grid_x * 5), 120 + (row * 60) + (grid_y * 5)),
                                        square_size))
        draw_numbers(display, board, GREEN)
        draw_numbers(display, puzzle_copy, DARK_BLUE)
        pygame.display.update()

    return False


def generate_puzzle() -> None:
    global puzzle_num
    global puzzle
    global puzzle_copy

    puzzles = [[[3, 0, 6, 5, 0, 8, 4, 0, 0],
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

    if puzzle_num == 3:
        puzzle_num = -1
    puzzle_num += 1
    puzzle = copy.deepcopy(puzzles[puzzle_num])
    puzzle_copy = copy.deepcopy(puzzles[puzzle_num])


def draw_buttons(display: pygame.display, mouse_pos: pygame.mouse) -> None:
    button_font = pygame.font.SysFont('freesansbold.ttf', 48)

    for i in range(3):
        if 730 < mouse_pos[0] < 970 and 120 + (110 * i) < mouse_pos[1] < 190 + (110 * i):
            pygame.draw.rect(display, LIGHT_BLUE, ((725, 115 + (110 * i)), (250, 80)))
        pygame.draw.rect(display, WHITE, ((730, 120 + (110 * i)), (240, 70)))
    display.blit(button_font.render('NEW PUZZLE', True, DARK_BLUE), (742, 142))
    display.blit(button_font.render('SOLVE', True, DARK_BLUE), (796, 252))
    display.blit(button_font.render('QUICK SOLVE', True, DARK_BLUE), (738, 361))

    # Speed button
    draw_speed(display, mouse_pos)


def draw_speed(display, mouse_pos) -> None:
    colors = [(speed_1_col, RED), (speed_2_col, ORANGE), (speed_3_col, YELLOW), (speed_4_col, YELLOW_GREEN),
              (speed_5_col, GREEN)]
    button_font = pygame.font.SysFont('freesansbold.ttf', 48)
    for i in range(5):
        if 688 + (65 * i) < mouse_pos[0] <= 754 + (65 * i) and 550 < mouse_pos[1] < 605:
            pygame.draw.rect(display, WHITE, ((689, 545), (65 * (i + 1), 65)))
    for i in range(5):
        if colors[i][0]:
            pygame.draw.rect(display, colors[i][1], ((694 + (i * 65), 550), (55, 55)))
        else:
            pygame.draw.rect(display, GRAY, ((694 + (i * 65), 550), (55, 55)))
    speed_text_surface = button_font.render('SPEED', True, WHITE)
    display.blit(speed_text_surface, (796, 500))


def main():
    pygame.init()
    running = True

    while running:
        display = pygame.display.set_mode((1080, 720))
        display.fill(DARK_BLUE)
        draw_empty_board(display)
        draw_numbers(display, puzzle, DARK_BLUE)
        mouse_pos = pygame.mouse.get_pos()
        draw_buttons(display, mouse_pos)

        # Get button presses
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                # Pressed 'SOLVE' button
                if 730 < mouse_pos[0] < 970 and 230 < mouse_pos[1] < 300:
                    solve_visual(puzzle)

                # Pressed the 'SOLVE INSTANTLY' button
                if 730 < mouse_pos[0] < 970 and 340 < mouse_pos[1] < 410:
                    button_font = pygame.font.SysFont('freesansbold.ttf', 48)
                    r = pygame.draw.rect(display, WHITE, ((730, 340), (240, 70)))
                    display.blit(button_font.render('SOLVING...', True, DARK_BLUE), (768, 360))
                    pygame.display.update(r)
                    solver.solve(puzzle)

                # Pressed 'NEW PUZZLE' button
                if 730 < mouse_pos[0] < 970 and 120 < mouse_pos[1] < 190:
                    generate_puzzle()

                # Pressed the speed buttons
                global speed_2_col
                global speed_3_col
                global speed_4_col
                global speed_5_col
                global SPEED

                if 688 < mouse_pos[0] < 1019 and 550 < mouse_pos[1] < 605:
                    speed_2_col = False
                    speed_3_col = False
                    speed_4_col = False
                    speed_5_col = False
                    SPEED = 30
                if 753 < mouse_pos[0] < 1019 and 550 < mouse_pos[1] < 605:
                    speed_2_col = True
                    SPEED = 60
                if 823 < mouse_pos[0] < 1019 and 550 < mouse_pos[1] < 605:
                    speed_3_col = True
                    SPEED = 120
                if 888 < mouse_pos[0] < 1019 and 550 < mouse_pos[1] < 605:
                    speed_4_col = True
                    SPEED = 240
                if 953 < mouse_pos[0] < 1019 and 550 < mouse_pos[1] < 605:
                    speed_5_col = True
                    SPEED = -1
        pygame.display.update()


main()
