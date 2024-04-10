import math
import statistics
from collections import namedtuple
from functools import wraps
import time
import random
from itertools import groupby
import haversine as haversine
from geopy import distance
from constants import BUSY_STOP, EUCLIDEAN, MANHATTAN

Cords = namedtuple("Cords", ["X", "Y"])
NextStop = namedtuple("NextStop", ["name", "cords", "line", "departure", "arrival"])


def convert_to_seconds(time_str):
    h, m, s = map(int, time_str.split(':'))
    return h * 3600 + m * 60 + s


def convert_to_time_string(total_seconds):
    h = total_seconds // 3600
    m = (total_seconds % 3600) // 60
    s = total_seconds % 60
    return '{:02d}:{:02d}:{:02d}'.format(h, m, s)


def update_start_pos(graph):
    for start, data in graph.items():
        start_pos_list = list(data["start_pos"])
        if len(start_pos_list) > 0:
            avg_pos = Cords(statistics.mean(pos.X for pos in start_pos_list),
                            statistics.mean(pos.Y for pos in start_pos_list))
            data["start_pos"] = avg_pos


# Czas obliczeń liczony od wczytania danych do uzyskania rozwiązania
def time_taken_dijkstra(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.perf_counter()
        result = func(*args, **kwargs)
        end_time = time.perf_counter()
        total_time = end_time - start_time
        print(f'Function {func.__name__} Took {total_time:.4f} seconds')
        return result

    return wrapper

def time_taken_tabu_search(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.perf_counter()
        result = func(*args, **kwargs)
        end_time = time.perf_counter()
        total_time = end_time - start_time
        print(f'Function {func.__name__} Took {total_time:.4f} seconds')
        return result

    return wrapper


a_star_evaluation_times = {}
a_star_cost_values = {}

def time_taken_a_star(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.perf_counter()
        result = func(*args, **kwargs)
        cost = result[1]
        heuristic = args[4]
        end_time = time.perf_counter()
        total_time = end_time - start_time
        if heuristic.__name__ not in a_star_evaluation_times:
            a_star_evaluation_times[heuristic.__name__] = []
            a_star_cost_values[heuristic.__name__] = []
        a_star_evaluation_times[heuristic.__name__].append(total_time)
        a_star_cost_values[heuristic.__name__].append(cost)
        print(f'Function {func.__name__} Took {total_time:.4f} seconds')
        return result

    return wrapper

def print_a_star_results():
    header = f"{'Heuristic':<25}{'Average time':<25}{'Average cost':<25}"
    print(header)
    print('-' * len(header))
    for heuristic_name in a_star_evaluation_times:
        times = a_star_evaluation_times[heuristic_name]
        costs = a_star_cost_values[heuristic_name]
        print(f"{heuristic_name:<25}{round(sum(times) / len(times), 8):<25}"
              f"{round(sum(costs) / len(costs), 8):<25}")

def print_stops(path):
    groups = groupby(path, key=lambda stop: stop[1])
    print('-' * 106)
    print(f"{'Line':<10}{'Start':<50}{'End':<50}")
    print('-' * 106)

    for line, group in groups:
        group_list = list(group)
        start = group_list[0]
        end = group_list[-1]
        print(f"{line:<10}{start[2]:<10}{start[0]:<40}{end[3]:<10}{end[4]:<40}")

    print('-' * 106)


def print_results_dijkstra(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        cost, path, start_time = func(*args, **kwargs)
        print("Starting time: ", convert_to_time_string(start_time))
        print("Total cost:", convert_to_time_string(cost))
        print_stops(path)
        print()
        return cost, path

    return wrapper


def print_results_astar(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        heuristic_fn = kwargs.get('heuristic_fn')
        cost, path, start_time = func(*args, **kwargs)
        print("Starting time: ", convert_to_time_string(start_time))
        print(f"Total cost for {heuristic_fn.__name__} heuristic: {convert_to_time_string(cost)}")
        print_stops(path)
        print()
        return cost, path

    return wrapper


def haversine_distance(goal, current):
    current_cords = goal["start_pos"]
    end_cords = current["start_pos"]
    return haversine.haversine(current_cords, end_cords) * 1000


def geo_distance(current, goal):
    current_cords = current["start_pos"]
    end_cords = goal["start_pos"]
    return distance.distance(current_cords, end_cords).km


def line_change_heuristic(neighbor_node, neighbor, goal_lines_dict):
    is_goal_line = 0 if neighbor.line in goal_lines_dict else 1000
    return BUSY_STOP - len(neighbor_node["next_stop"]) + is_goal_line


def manhattan_distance(a, b):
    a = a["start_pos"]
    b = b["start_pos"]
    return sum([abs(x - y) for x, y in zip(a, b)]) * MANHATTAN


def euclidean_distance(a, b):
    a = a["start_pos"]
    b = b["start_pos"]
    return math.sqrt(sum([(x - y) ** 2 for x, y in zip(a, b)])) * EUCLIDEAN


def two_opt(current):
    prev = random.randint(0, len(current) - 1)
    curr = random.randint(0, len(current) - 1)
    current[curr], current[prev] = current[prev], current[curr]
    return current, (prev, current)


