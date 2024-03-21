from constants import FILE_PATH
import pandas as pd
from utils import Cords, NextStop, convert_to_seconds, update_start_pos


def load_data():
    with open(FILE_PATH, "r") as file:
        df = pd.read_csv(file, dtype={"line": str})
    graph = {}
    for _, row in df.iterrows():
        start = row["start_stop"]
        end = row["end_stop"]
        start_pos = Cords(row["start_stop_lat"], row["start_stop_lon"])
        end_pos = Cords(row["end_stop_lat"], row["end_stop_lon"])
        next_stop = NextStop(row["end_stop"], end_pos, row["line"],
                             convert_to_seconds(row["departure_time"]),
                             convert_to_seconds(row["arrival_time"]))

        if start not in graph:
            graph[start] = {
                "start_pos": set(),
                "next_stop": set()
            }
        if end not in graph:
            graph[end] = {
                "start_pos": set(),
                "next_stop": set()
            }

        graph[start]["start_pos"].add(start_pos)
        graph[start]["next_stop"].add(next_stop)
        graph[end]["start_pos"].add(end_pos)

    update_start_pos(graph)
    return graph
