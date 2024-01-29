from tictactoe import actions, player, X, O, EMPTY


def TEST_actions():
    # board = [[None, None, None], [None, None, None], [None, None, None]]
    board = [[X, X, X], [X, X, X], [X, None, None]]
    print(actions(board))


def TEST_player():
    board = [[X, X, O], [O, EMPTY, EMPTY], [EMPTY, EMPTY, EMPTY]]
    print(player(board))


# TEST_actions()
TEST_player()
