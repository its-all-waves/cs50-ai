"""
Tic Tac Toe Player
"""

import math
from copy import deepcopy

X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY], [EMPTY, EMPTY, EMPTY], [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.

    Counts and returns the player with the least moves currently on the board.

    TODO FIX
        :( player returns X after four moves
        expected "X", not "O"
    """
    if terminal(board):
        return None

    # X always goes first (rule)
    if board == initial_state():
        return X

    num_X, num_O = 0, 0
    for row in board:
        num_X += row.count(X)
        num_O += row.count(O)

    # since X goes first, X count > O count if O's move, X count == O count if X's move
    return O if num_X > num_O else X


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    if terminal(board):  # DEBUG - UNCOMMENT ME
        return None

    # row is [val, val, val]
    # col is X or O or EMPTY

    # return coodinates of all empty cells
    range_3 = range(3)
    return set((i, j) for i in range_3 for j in range_3 if board[i][j] == EMPTY)


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    i, j = action
    if i > 3 or i < 0 or j > 3 or j < 0:
        raise IndexError("There are no negative coordinates.")

    if board[i][j] != EMPTY:
        raise Exception("Invalid action. The cell is already occupied.")

    # perform player's action on copy / place player's symbol at given position
    player_symbol = player(board)
    new_board_state = deepcopy(board)
    new_board_state[i][j] = player_symbol

    # return a copy the board, as if player who's turn it is does action
    return new_board_state


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    # check for 3 in a row in a row
    for row in board:
        if row == [X, X, X]:
            return X
        if row == [O, O, O]:
            return O

    # check for 3 in a row in a col
    col0_count, col1_count, col2_count = 0, 0, 0
    for row in board:
        if row[0] == X:
            col0_count += 1
        if row[1] == X:
            col1_count += 1
        if row[2] == X:
            col2_count += 1
    if col0_count == 3 or col1_count == 3 or col2_count == 3:
        return X

    col0_count, col1_count, col2_count = 0, 0, 0
    for row in board:
        if row[0] == O:
            col0_count += 1
        if row[1] == O:
            col1_count += 1
        if row[2] == O:
            col2_count += 1
    if col0_count == 3 or col1_count == 3 or col2_count == 3:
        return O

    # check for 3 in a row on a diagonal
    LR_diagonal_count = (board[0][0], board[1][1], board[2][2])
    RL_diagonal_count = (board[0][2], board[1][1], board[2][0])
    if LR_diagonal_count == (X, X, X) or RL_diagonal_count == (X, X, X):
        return X
    if LR_diagonal_count == (O, O, O) or RL_diagonal_count == (O, O, O):
        return O

    return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    # if there's a winner or no empty cells
    # TODO ??? the other case(s)
    there_is_a_winner = bool(winner(board))
    all_cells_are_occupied = all(cell != EMPTY for row in board for cell in row)
    return True if there_is_a_winner or all_cells_are_occupied else False


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    _winner = winner(board)
    return 1 if _winner == X else -1 if _winner == O else 0


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    raise NotImplementedError
