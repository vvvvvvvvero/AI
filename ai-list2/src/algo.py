def minimax(state, depth, maximizing_now, heuristic):
    node_count = 1

    if depth == 0:
        return heuristic(state, state.current_player), None, node_count

    if maximizing_now:
        max_eval = float('-inf')
        best_move = None
        total_nodes = 0

        for move in state.generate_moves():
            state.make_move(move)
            state.current_player = 2 if state.current_player == 1 else 1

            evaluation, _, nodes_visited = minimax(state, depth - 1, False, heuristic)
            total_nodes += nodes_visited

            state.current_player = 2 if state.current_player == 1 else 1
            state.undo_move(move)

            if evaluation > max_eval:
                max_eval = evaluation
                best_move = move

        return max_eval, best_move, total_nodes + node_count
    else:
        min_eval = float('inf')
        total_nodes = 0

        for move in state.generate_moves():
            state.make_move(move)
            state.current_player = 2 if state.current_player == 1 else 1

            evaluation, _, nodes_visited = minimax(state, depth - 1, True, heuristic)
            total_nodes += nodes_visited

            state.current_player = 2 if state.current_player == 1 else 1
            state.undo_move(move)
            min_eval = min(min_eval, evaluation)
        return min_eval, None, total_nodes + node_count


def minimax_alpha_beta(state, depth, alpha, beta, maximizing_now, heuristic):
    node_count = 1

    if depth == 0:
        return heuristic(state, state.current_player), None, node_count

    if maximizing_now:
        max_eval = float('-inf')
        best_move = None
        total_nodes = 0

        for move in state.generate_moves():
            state.make_move(move)
            state.current_player = 2 if state.current_player == 1 else 1

            evaluation, _, nodes_visited = minimax_alpha_beta(state, depth - 1, alpha, beta, False, heuristic)
            total_nodes += nodes_visited

            state.current_player = 2 if state.current_player == 1 else 1
            state.undo_move(move)
            if evaluation > max_eval:
                max_eval = evaluation
                best_move = move
            alpha = max(alpha, evaluation)
            if beta <= alpha:
                break
        return max_eval, best_move, total_nodes + node_count
    else:
        min_eval = float('inf')
        total_nodes = 0

        for move in state.generate_moves():
            state.make_move(move)
            state.current_player = 2 if state.current_player == 1 else 1

            evaluation, _, nodes_visited = minimax_alpha_beta(state, depth - 1, alpha, beta, True, heuristic)
            total_nodes += nodes_visited

            state.current_player = 2 if state.current_player == 1 else 1
            state.undo_move(move)

            min_eval = min(min_eval, evaluation)
            beta = min(beta, evaluation)
            if beta <= alpha:
                break
        return min_eval, None, total_nodes + node_count
