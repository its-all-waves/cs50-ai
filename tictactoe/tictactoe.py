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
    return [
        [EMPTY, EMPTY, EMPTY],
        [EMPTY, EMPTY, EMPTY],
        [EMPTY, EMPTY, EMPTY],
    ]


def player(board):
    """
    Returns player who has the next turn on a board.
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
        return set()

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
        raise IndexError("Coordinates of moves must be in range 0-2, inclusive.")

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

    all_X = [X, X, X]
    all_O = [O, O, O]

    # check for 3 in a row in a row
    row_0 = board[0]
    row_1 = board[1]
    row_2 = board[2]
    if row_0 == all_X or row_1 == all_X or row_2 == all_X:
        return X
    if row_0 == all_O or row_1 == all_O or row_2 == all_O:
        return O

    # check for 3 in a row in a col
    col_0 = [board[0][0], board[1][0], board[2][0]]
    col_1 = [board[0][1], board[1][1], board[2][1]]
    col_2 = [board[0][2], board[1][2], board[2][2]]
    if col_0 == all_X or col_1 == all_X or col_2 == all_X:
        return X
    if col_0 == all_O or col_1 == all_O or col_2 == all_O:
        return O

    # check for 3 in a row on a diagonal
    diag_LR = [board[0][0], board[1][1], board[2][2]]
    diag_RL = [board[0][2], board[1][1], board[2][0]]
    if diag_LR == all_X or diag_RL == all_X:
        return X
    if diag_LR == all_O or diag_RL == all_O:
        return O

    return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    there_is_a_winner = bool(winner(board))
    all_cells_are_occupied = all(cell != EMPTY for row in board for cell in row)
    return there_is_a_winner or all_cells_are_occupied


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    _winner = winner(board)
    return 1 if _winner == X else -1 if _winner == O else 0


def minimax(board):
    """
    Returns the optimal action (i, j) for the current player on the board.
    """
    if not (player_turn := player(board)):
        return None

    if player_turn == X:
        X_best_action = None
        X_best_util = float("-inf")

        for X_action in actions(board):
            board_after_X_action = result(board, X_action)
            O_best_util = min_value(board_after_X_action)
            if O_best_util > X_best_util:
                X_best_util = O_best_util
                X_best_action = X_action

        return X_best_action

    if player_turn == O:
        O_best_action = None
        O_best_util = float("inf")

        for O_action in actions(board):
            board_after_O_action = result(board, O_action)
            X_best_util = max_value(board_after_O_action)
            if X_best_util < O_best_util:
                O_best_util = X_best_util
                O_best_action = O_action

        return O_best_action


def max_value(board):
    """Helper for minimax()"""
    if terminal(board):
        return utility(board)

    X_best_util = float("-inf")
    for X_action in actions(board):
        board_after_X_action = result(board, X_action)
        O_best_util = min_value(board_after_X_action)
        if O_best_util > X_best_util:
            X_best_util = O_best_util

    return X_best_util


def min_value(board):
    """Helper for minimax()"""
    if terminal(board):
        return utility(board)

    O_best_util = float("inf")
    for O_action in actions(board):
        board_after_O_action = result(board, O_action)
        X_best_util = max_value(board_after_O_action)
        if X_best_util < O_best_util:
            O_best_util = X_best_util

    return O_best_util
