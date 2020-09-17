import time


def is_valid(board: list, row: int, col: int, num: int) -> bool:
    """Check to see if a specified number in the board is a valid number
    (does not repeat horizontally, vertically, or in the same 9-square grid)."""

    # Check the row.
    for i in board[row]:
        if i == num:
            return False

    # Check the column.
    for i in range(9):
        if board[i][col] == num:
            return False

    # Check the square.
    m = row // 3
    n = col // 3
    for i in range(3):
        for j in range(3):
            if board[i + (3 * m)][j + (3 * n)] == num:
                return False

    return True


def find_empty(board: list) -> (int, int) or None:
    """Find the next empty spot in the board.
    Return (row, col) or None if no empty spots are found."""

    for row in range(9):
        for col in range(9):
            if board[row][col] == 0:
                return row, col
    return None


def solve(board: list) -> bool:
    """Solve the sudoku board recursively using a backtracking algorithm."""

    coordinates = find_empty(board)
    if not coordinates:
        return True

    row, col = coordinates
    for i in range(1, 10):
        if is_valid(board, row, col, i):
            board[row][col] = i

            if solve(board):
                return True

        board[row][col] = 0

    return False


def print_board(board: list) -> None:
    """Formats and prints out the sudoku board."""
    print()
    for j, row in enumerate(board, 1):
        for i, n in enumerate(row, 1):
            print(n, ' ', end='')
            if i == 3 or i == 6:
                print('|  ', end='')
        print()
        if j % 3 == 0 and j != 9:
            print('- - - - - - - - - - - - - - - -')
