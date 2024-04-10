import pandas as pd
from constants import THE_BUSIEST_STOPS
from load_data import load_data
from dijkstra import shortest_path
from a_star import execute_astar, a_star
import random
import csv

from tabu_search import tabu_search
from utils import geo_distance, haversine_distance, manhattan_distance, euclidean_distance, print_a_star_results


def dijkstra(graph, start_stop, end_stop, appearance_time):
    shortest_path(graph, start_stop, end_stop, appearance_time)


def astar(graph, start_stop, end_stop, appearance_time, option):
    execute_astar(graph, start_stop, end_stop, appearance_time, option)


def the_busiest_stops(graph):
    list_of_stops = []
    for stop in graph:
        list_of_stops.append((stop, len(graph[stop]["next_stop"])))
    list_of_stops.sort(key=lambda x: x[1], reverse=True)
    with open('../data/the_busiest_stops.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Stop", "Number of connections"])
        for stop in list_of_stops:
            writer.writerow(stop)


def check_a_star_heuristics(graph, start_stop, end_stop, appearance_time):
    heuristics = [manhattan_distance, haversine_distance, euclidean_distance, geo_distance]
    for heuristic in heuristics:
        try:
            a_star(graph, start_stop, end_stop, appearance_time, heuristic_fn=heuristic)
        except KeyError:
            pass


def check_heuristics(n, graph):
    df = pd.read_csv(THE_BUSIEST_STOPS)
    stations = df["Stop"].tolist()
    for _ in range(n):
        start_stop, end_stop = random.sample(stations, 2)
        check_a_star_heuristics(graph, start_stop, end_stop, "10:00:00")
    print_a_star_results()


if __name__ == '__main__':
    connection_graph = load_data()

    # start = "PL. GRUNWALDZKI"
    # end = "Tramwajowa"
    # time = "10:00:00"
    start = "PORT LOTNICZY"
    end = "Swojczyce"
    time = "08:28:00"

    # dijkstra(connection_graph, start, end, time)
    # astar(connection_graph, start, end, time, "t")
    # astar(connection_graph, start, end, time, "p")
    # test_heuristics(5000, connection_graph)
    # print(haversine_distance(connection_graph[start], connection_graph[end]))
    # print(geo_distance(connection_graph[start], connection_graph[end]))
    # print(manhattan_distance(connection_graph[start], connection_graph[end]))
    # print(euclidean_distance(connection_graph[start], connection_graph[end]))

    # L = ["PL. GRUNWALDZKI", "DWORZEC NADODRZE", "Żmudzka", "ZOO", "Zakładowa",
    #      "Wyszyńskiego", "Kominiarska", "Kwidzyńska", "Rdestowa", "Tramwajowa", "Volvo", "Śrubowa"]
    L = ["PL. GRUNWALDZKI", "ZOO", "Tramwajowa"]

    tabu_search(connection_graph, "Reja", L, time, "t")
