import math
import numpy as np
from halma import Halma
from board import create_game_board

def euclidean_distance_heuristic_1(state, current_player):
    player_target = (15, 15) if current_player == 1 else (0, 0)
    target_zone = {(11, 15), (11, 14), (13, 13), (15, 11), (14, 11)} if current_player == 1 else {(0, 4), (1, 4), (2, 2), (4, 0), (4, 1)}
    player_score = 0

    for y in range(len(state.board)):
        for x in range(len(state.board)):
            current_piece = state.board[x][y]
            if current_piece == current_player:
                dx, dy = x - player_target[0], y - player_target[1]
                distance = math.sqrt(dx * dx + dy * dy)
                player_score += 20 - distance
                if distance <= 4:
                    player_score += 10
                if (x, y) in target_zone:
                    player_score += 15

    return player_score

def euclidean_distance_heuristic_2(state, current_player):
    target_x, target_y = (15, 15) if current_player == 1 else (0, 0)

    edges_player_1 = {(11, 14): 9, (11, 15): 4, (12, 15): 4, (13, 15): 5, (14, 15): 6, (15, 15): 10,
                      (15, 14): 6, (15, 13): 5, (15, 12): 4, (15, 11): 4, (14, 11): 9}
    edges_player_2 = {(1, 0): 6, (2, 0): 5, (3, 0): 4, (4, 0): 4, (4, 1): 9, (0, 0): 10, (0, 1): 6,
                      (0, 2): 5, (0, 3): 4, (0, 4): 4, (1, 4): 9}

    edge_bonuses = edges_player_1 if current_player == 1 else edges_player_2

    player_score = 0

    for x in range(len(state.board)):
        for y in range(len(state.board)):
            if state.board[x][y] == current_player:
                distance = math.sqrt((x - target_x) ** 2 + (y - target_y) ** 2)
                player_score += 20 - distance

                if (x, y) in edge_bonuses:
                    player_score += edge_bonuses[(x, y)]

    return player_score


if __name__ == '__main__':
    initial_board = create_game_board()












