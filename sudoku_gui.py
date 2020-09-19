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
RED = (150, 25, 25)
RED_2 = (148, 55, 47)
ORANGE = (199, 130, 66)
YELLOW = (207, 186, 68)
YELLOW_GREEN = (200, 209, 67)
GREEN_2 = (81, 138, 45)
GREEN = (25, 140, 25)

speed_1_col = RED_2
speed_2_col = ORANGE
speed_3_col = YELLOW
speed_4_col = GRAY
speed_5_col = GRAY

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
                if 694 < mouse_pos[0] < 1019 and 550 < mouse_pos[1] < 605:
                    pygame.draw.rect(display, RED, ((689, 545), (65, 65)))
                    speed_2_col = GRAY
                    speed_3_col = GRAY
                    speed_4_col = GRAY
                    speed_5_col = GRAY
                    SPEED = 30
                if 753 < mouse_pos[0] < 1019 and 550 < mouse_pos[1] < 605:
                    speed_2_col = ORANGE
                    SPEED = 90
                if 823 < mouse_pos[0] < 1019 and 550 < mouse_pos[1] < 605:
                    speed_3_col = YELLOW
                    SPEED = 150
                if 888 < mouse_pos[0] < 1019 and 550 < mouse_pos[1] < 605:
                    speed_4_col = YELLOW_GREEN
                    SPEED = 250
                if 953 < mouse_pos[0] < 1019 and 550 < mouse_pos[1] < 605:
                    speed_5_col = GREEN
                    SPEED = -1
                # Pressed the 'SOLVE INSTANTLY' button
                if 730 < mouse_pos[0] < 970 and 340 < mouse_pos[1] < 410:
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
        draw_numbers(display, board, GREEN_2)
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
    solve_button_surface = button_font.render('SOLVE', True, DARK_BLUE)
    new_puzzle_button_surface = button_font.render('NEW PUZZLE', True, DARK_BLUE)

    button_font_2 = pygame.font.SysFont('freesansbold.ttf', 24)
    solve_instant_button_surface = button_font.render('SOLVE', True, DARK_BLUE)
    solve_instant_2_button_surface = button_font.render('INSTANTLY', True, DARK_BLUE)

    # New puzzle button
    if 730 < mouse_pos[0] < 970 and 120 < mouse_pos[1] < 190:
        pygame.draw.rect(display, LIGHT_BLUE, ((725, 115), (250, 80)))
    pygame.draw.rect(display, WHITE, ((730, 120), (240, 70)))
    display.blit(new_puzzle_button_surface, (742, 142))

    # Solve button
    if 730 < mouse_pos[0] < 970 and 230 < mouse_pos[1] < 300:
        pygame.draw.rect(display, LIGHT_BLUE, ((725, 225), (250, 80)))
    pygame.draw.rect(display, WHITE, ((730, 230), (240, 70)))
    display.blit(solve_button_surface, (796, 252))

    if 730 < mouse_pos[0] < 970 and 340 < mouse_pos[1] < 410:
        pygame.draw.rect(display, LIGHT_BLUE, ((725, 335), (250, 80)))
    pygame.draw.rect(display, WHITE, ((730, 340), (240, 70)))
    display.blit(solve_instant_button_surface, (796, 342))
    display.blit(solve_instant_2_button_surface, (758, 372))

    # Speed button
    draw_speed(display, mouse_pos)


def draw_speed(display, mouse_pos) -> None:
    button_font = pygame.font.SysFont('freesansbold.ttf', 48)
    if 694 < mouse_pos[0] < 754 and 550 < mouse_pos[1] < 605:
        pygame.draw.rect(display, WHITE, ((689, 545), (65, 65)))
    if 753 < mouse_pos[0] < 824 and 550 < mouse_pos[1] < 605:
        pygame.draw.rect(display, WHITE, ((689, 545), (130, 65)))
    if 823 < mouse_pos[0] < 889 and 550 < mouse_pos[1] < 605:
        pygame.draw.rect(display, WHITE, ((689, 545), (195, 65)))
    if 888 < mouse_pos[0] < 954 and 550 < mouse_pos[1] < 605:
        pygame.draw.rect(display, WHITE, ((689, 545), (260, 65)))
    if 953 < mouse_pos[0] < 1019 and 550 < mouse_pos[1] < 605:
        pygame.draw.rect(display, WHITE, ((689, 545), (325, 65)))

    speed_text_surface = button_font.render('SPEED', True, WHITE)
    display.blit(speed_text_surface, (796, 500))
    pygame.draw.rect(display, speed_1_col, ((694, 550), (55, 55)))
    pygame.draw.rect(display, speed_2_col, ((759, 550), (55, 55)))
    pygame.draw.rect(display, speed_3_col, ((824, 550), (55, 55)))
    pygame.draw.rect(display, speed_4_col, ((889, 550), (55, 55)))
    pygame.draw.rect(display, speed_5_col, ((954, 550), (55, 55)))


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
                if 694 < mouse_pos[0] < 1019 and 550 < mouse_pos[1] < 605:
                    pygame.draw.rect(display, RED, ((689, 545), (65, 65)))
                    speed_2_col = GRAY
                    speed_3_col = GRAY
                    speed_4_col = GRAY
                    speed_5_col = GRAY
                    SPEED = 30
                if 753 < mouse_pos[0] < 1019 and 550 < mouse_pos[1] < 605:
                    speed_2_col = ORANGE
                    SPEED = 60
                if 823 < mouse_pos[0] < 1019 and 550 < mouse_pos[1] < 605:
                    speed_3_col = YELLOW
                    SPEED = 120
                if 888 < mouse_pos[0] < 1019 and 550 < mouse_pos[1] < 605:
                    speed_4_col = YELLOW_GREEN
                    SPEED = 240
                if 953 < mouse_pos[0] < 1019 and 550 < mouse_pos[1] < 605:
                    speed_5_col = GREEN
                    SPEED = -1
        pygame.display.update()


main()
