import numpy as np

MOVE_DIRECTIONS = [(-1, -1), (-1, 1), (1, -1), (1, 1), (1, 0), (-1, 0), (0, 1), (0, -1)]
JUMP_DIRECTIONS = [(-2, -2), (-2, 2), (2, -2), (2, 2), (2, 0), (-2, 0), (0, 2), (0, -2)]


class Halma:
    def __init__(self, board, current_player):
        self.board = board
        self.current_player = current_player

    def generate_moves(self):
        moves = []
        temp_moves = []
        for x in range(len(self.board)):
            for y in range(len(self.board)):
                if self.board[x][y] == self.current_player:
                    temp_moves = self.generate_moves_for_position(x, y)
                    temp_moves = consolidate_moves(temp_moves, (x, y))
                    moves.extend(temp_moves)
        moves = set(moves)
        return list(moves)

    def generate_moves_for_position(self, x, y, visited=None, is_recursion_call=False, is_jump=False):
        if visited is None:
            visited = set()
        visited.add((x, y))

        if not is_recursion_call and self.board[x][y] != self.current_player:
            return []

        moves = []
        for dx, dy in MOVE_DIRECTIONS:
            new_x, new_y = x + dx, y + dy
            jump_x, jump_y = new_x + dx, new_y + dy
            if 0 <= new_x < len(self.board) and 0 <= new_y < len(self.board) and (new_x, new_y) not in visited:
                if self.board[new_x][new_y] == 0 and not is_jump:  # Simple move
                    moves.append(Move((x, y), (new_x, new_y)))
                elif 0 <= jump_x < len(self.board) and 0 <= jump_y < len(self.board) and (jump_x, jump_y) not in visited:
                    if self.board[new_x][new_y] in [1, 2] and self.board[jump_x][jump_y] == 0:  # Jump
                        moves.append(Move((x, y), (jump_x, jump_y)))
                        moves.extend(self.generate_moves_for_position(jump_x, jump_y, visited.copy(), True, True))
        return moves

    def make_move(self, move):
        self.board[move.end[0]][move.end[1]] = self.current_player
        self.board[move.start[0]][move.start[1]] = 0

    def undo_move(self, move):
        self.board[move.start[0]][move.start[1]] = self.current_player
        self.board[move.end[0]][move.end[1]] = 0

    def __str__(self):
        return str(self.board)

    def __repr__(self):
        return self.__str__()


class Move:
    def __init__(self, start, end):
        self.start = start
        self.end = end

    def is_legal_move(self, state):
        start_x, start_y = self.start
        end_x, end_y = self.end

        if state.board[start_x][start_y] != state.current_player or state.board[end_x][end_y] != 0:
            return False

        if abs(end_x - start_x) <= 1 and abs(end_y - start_y) <= 1:
            return True

        return self._check_jumps(start_x, start_y, end_x, end_y, state, set())

    def _check_jumps(self, current_x, current_y, end_x, end_y, state, visited):
        if (current_x, current_y) == (end_x, end_y):
            return True
        visited.add((current_x, current_y))

        for dir_x, dir_y in JUMP_DIRECTIONS:
            next_x, next_y = current_x + dir_x, current_y + dir_y
            mid_x, mid_y = current_x + dir_x // 2, current_y + dir_y // 2

            if 0 <= next_x < len(state.board) and 0 <= next_y < len(state.board) and (next_x, next_y) not in visited:
                if state.board[next_x][next_y] == 0 and state.board[mid_x][mid_y] in [1, 2]:
                    if self._check_jumps(next_x, next_y, end_x, end_y, state, visited):
                        return True
        return False

    def __str__(self):
        return f"{self.start} -> {self.end}"

    def __repr__(self):
        return self.__str__()


def consolidate_moves(move_list, origin):
    reset_moves = [Move(origin, move.end) for move in move_list]
    return reset_moves


if __name__ == '__main__':
    initial_board = np.zeros((16, 16), dtype=int)

    # Set up a simple scenario
    initial_board[0][0] = 1
    initial_board[1][1] = 1
    initial_board[2][1] = 1

    initial_board[3][3] = 2
    initial_board[2][3] = 2
    initial_board[3][2] = 2

    print(initial_board)

    game = Halma(initial_board, 1)
    generated_moves = game.generate_moves()
    print(generated_moves)
