import time
from halma import Halma
from board import check_the_winner, create_game_board
from algo import minimax_alpha_beta, minimax
from heuristics import (euclidean_distance_heuristic_1, euclidean_distance_heuristic_2)

NUM_OF_GAMES = 1
DEPTH = 2

def check_alpha_beta(first_player_heuristic, second_player_heuristic, file_name="task.txt"):
    result_file = open(f"results/{file_name}", "w")

    for i in range(NUM_OF_GAMES):
        board = create_game_board()
        state = Halma(board, 1)
        depth = DEPTH
        result_file.write(f"Game {i + 1}\n")
        print(f"Game {i + 1}")

        game_round = 0
        total_nodes = 0

        start_time = time.time()

        while True:
            print(f"Round {game_round + 1}")
            print(state)

            _, ai1_move, visited_nodes = minimax_alpha_beta(state, depth, float('-inf'), float('inf'), True,
                                                            heuristic=first_player_heuristic)
            total_nodes += visited_nodes
            state.make_move(ai1_move)
            state.current_player = 2

            _, ai2_move, visited_nodes = minimax_alpha_beta(state, depth, float('-inf'), float('inf'), True,
                                                            heuristic=second_player_heuristic)
            total_nodes += visited_nodes
            state.make_move(ai2_move)
            state.current_player = 1

            win = check_the_winner(state.board)
            if win != 0:
                result_file.write(str(state))
                result_file.write("\n")
                result_file.write(f"Winner: {win}\n")
                print(f"Winner: {win}")
                break

            game_round += 1

        end_time = time.time()
        result_file.write(f"Moves: {game_round}\n")
        result_file.write(f"Time: {end_time - start_time}\n")
        result_file.write(f"Total nodes visited: {total_nodes}\n")
        result_file.write("\n")
        result_file.write("\n")


def check_minimax(first_player_heuristic, second_player_heuristic, file_name):
    experimental_file = open(f"results/{file_name}", "w")

    for i in range(3):
        board = create_game_board()
        state = Halma(board, 1)
        depth = 2
        experimental_file.write(f"Game {i + 1}\n")
        print(f"Game {i + 1}")

        start_time = time.time()

        game_round = 0
        total_nodes = 0

        while True:
            print(f"Round {game_round + 1}")
            print(state)

            _, ai1_move, visited_nodes = minimax(state, depth, True, heuristic=first_player_heuristic)
            total_nodes += visited_nodes
            state.make_move(ai1_move)
            state.current_player = 2

            _, ai2_move, visited_nodes = minimax(state, depth, True, heuristic=second_player_heuristic)
            total_nodes += visited_nodes
            state.make_move(ai2_move)
            state.current_player = 1

            win = check_the_winner(state.board)
            if win != 0:
                experimental_file.write(str(state))
                experimental_file.write("\n")
                experimental_file.write(f"Winner: {win}\n")
                print(f"Winner: {win}")
                break

            game_round += 1

        end_time = time.time()
        experimental_file.write(f"Moves: {game_round}\n")
        experimental_file.write(f"Time: {end_time - start_time}\n")
        experimental_file.write(f"Total nodes visited: {total_nodes}\n")
        experimental_file.write("\n")
        experimental_file.write("\n")


if __name__ == "__main__":
    check_minimax(euclidean_distance_heuristic_2, euclidean_distance_heuristic_2, "minimax_2.txt")



