import numpy as np

PLAYER1_STARTING_POSITIONS = [(0, 0), (0, 1), (0, 2), (0, 3), (0, 4), (1, 0), (1, 1), (1, 2), (1, 3), (1, 4), (2, 0),
                              (2, 1), (2, 2), (2, 3), (3, 0), (3, 1), (3, 2), (4, 0), (4, 1)]
PLAYER2_STARTING_POSITIONS = [(15, 15), (15, 14), (15, 13), (15, 12), (15, 11), (14, 15), (14, 14), (14, 13), (14, 12),
                              (14, 11), (13, 15), (13, 14), (13, 13), (13, 12), (12, 15), (12, 14), (12, 13), (11, 15),
                              (11, 14)]

def create_game_board():
    board = np.zeros((16, 16), dtype=int)

    for x, y in PLAYER1_STARTING_POSITIONS:
        board[x][y] = 1

    for x, y in PLAYER2_STARTING_POSITIONS:
        board[x][y] = 2

    return board

def check_the_winner(board):
    player1_target = PLAYER2_STARTING_POSITIONS
    player2_target = PLAYER1_STARTING_POSITIONS

    player1_count = 0
    player2_count = 0

    for x, y in player1_target:
        if board[x][y] == 1:
            player1_count += 1

    for x, y in player2_target:
        if board[x][y] == 2:
            player2_count += 1

    if player1_count == 19:
        return 1

    if player2_count == 19:
        return 2

    return 0


if __name__ == '__main__':
    my_board = create_game_board()
    print(my_board)

