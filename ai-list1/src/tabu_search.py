import math
import random

from utils import two_opt, convert_to_time_string
from a_star import execute_astar

def get_distances(graph, stops, start_time, opt):
    distances = {}
    total = 0
    for start_stop in stops:
        distances[start_stop] = {}
        for end_stop in stops:
            if start_stop == end_stop:
                distances[start_stop][end_stop] = 0
                continue
            dist = execute_astar(graph, start_stop, end_stop, start_time, opt)[0]
            distances[start_stop][end_stop] = dist
            total += dist

    return distances, total


def tabu_search(graph, start_stop, stops, time, opt):
    stops.append(start_stop)
    n_stops = len(stops)
    distances, total = get_distances(graph, stops, time, opt)

    max_iterations = n_stops ** 2
    tabu_list = []

    no_improve_counter = 0
    improve_limit = math.floor(2 * math.sqrt(max_iterations))

    tabu_tenure = n_stops

    current_solution = stops
    random.shuffle(current_solution)

    best_solution = current_solution[:]
    best_solution_cost = sum(
        [distances[current_solution[i]][current_solution[(i + 1) % n_stops]] for i in range(n_stops)])

    for iteration in range(max_iterations):
        if no_improve_counter > improve_limit:
            break
        best_neighbor = None
        best_neighbor_cost = float('inf')
        tabu_candidate = (None, None)

        aspiration_criteria = best_solution_cost * 0.5

        for i in range(n_stops):
            neighbor, move = two_opt(current_solution[:])
            neighbor_cost = sum([distances[neighbor[i]][neighbor[(i + 1) % n_stops]] for i in range(n_stops)])
            if move not in tabu_list or neighbor_cost < aspiration_criteria:
                if neighbor_cost < best_neighbor_cost:
                    best_neighbor = neighbor[:]
                    best_neighbor_cost = neighbor_cost
                    tabu_candidate = move

        if best_neighbor is not None:
            current_solution = best_neighbor[:]
            tabu_list.append(tabu_candidate)
            if len(tabu_list) > tabu_tenure:
                tabu_list.pop(0)
            if best_neighbor_cost < best_solution_cost:
                best_solution = best_neighbor[:]
                best_solution_cost = best_neighbor_cost
                no_improve_counter = 0
            else:
                no_improve_counter += 1

        print("Iteration {}: Best solution cost = {}".format(iteration, best_solution_cost))

    start_id = best_solution.index(start_stop)
    result = best_solution[start_id:] + best_solution[:start_id]
    print("Best solution: {}".format(result))
    print("Best solution cost: {}".format(convert_to_time_string(best_solution_cost)))
