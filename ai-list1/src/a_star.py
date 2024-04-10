import heapq
import utils


@utils.time_taken_a_star
def a_star_inner_time(graph, start, goal, time, heuristic_fn):
    goal_node = graph[goal]
    priority_queue = [(0, start)]  # lista otwartych węzłów
    visited = set()  # zbiór zamkniętych węzłów
    came_from = {start: None}
    cost_so_far = {start: 0}

    while priority_queue:
        _, current = heapq.heappop(priority_queue)
        if current == goal:
            break

        if current in visited:
            continue

        visited.add(current)
        current_cost = cost_so_far[current]

        # sprawdzamy sąsiadów przystanku
        for neighbor in (n for n in graph[current]["next_stop"] if
                         n.departure >= current_cost + time and n.name not in visited):
            new_cost = neighbor.arrival - time

            # jesli przystanek nie był odwiedzony lub nowy koszt jest mniejszy
            if neighbor.name not in cost_so_far or new_cost < cost_so_far[neighbor.name]:
                cost_so_far[neighbor.name] = new_cost
                came_from[neighbor.name] = current, neighbor.line, neighbor.departure, neighbor.arrival, neighbor.name
                priority = new_cost + heuristic_fn(goal_node, graph[neighbor.name])
                # print(new_cost, heuristic_fn(goal_node, graph[neighbor.name]))
                heapq.heappush(priority_queue, (priority, neighbor.name))

    return came_from, cost_so_far[goal]


@utils.time_taken_a_star
def a_star_inner_line(graph, start, goal, time, heuristic_fn):
    goal_lines_dict = {x.line: True for x in
                       graph[goal]["next_stop"]}  # ustawiamy true dla linii polaczanych z przystankiem docelowym
    priority_queue = [(0, start)]
    visited = set()
    came_from = {start: None}
    cost_so_far = {start: (0, 0, 0)}

    while priority_queue:
        _, current = heapq.heappop(priority_queue)

        if current in visited:
            continue
        visited.add(current)

        if current == goal:
            break
        current_cost = cost_so_far[current][0]
        current_time = cost_so_far[current][1]
        line = came_from[current][1] if came_from[current] else None

        filtered_stops = (n for n in graph[current]["next_stop"] if
                          n.departure >= current_time + time and n.name not in visited)

        for neighbor in filtered_stops:
            new_cost = (0 if line == neighbor.line else 1000) + current_cost
            new_time = neighbor.arrival - time
            priority = new_cost + new_time / 3 + heuristic_fn(graph[neighbor.name], neighbor, goal_lines_dict)

            if neighbor.name not in cost_so_far or priority < cost_so_far[neighbor.name][2] or priority == \
                    cost_so_far[neighbor.name][2] and new_time < cost_so_far[neighbor.name][1]:
                cost_so_far[neighbor.name] = new_cost, new_time, priority # koszt przystanku, czas przyjazdu, priorytet
                # print(cost_so_far)
                came_from[neighbor.name] = current, neighbor.line, neighbor.departure, neighbor.arrival, neighbor.name
                heapq.heappush(priority_queue, (priority, neighbor.name))
    return came_from, cost_so_far[goal][1]


@utils.print_results_astar
def a_star(graph, start, goal, time, heuristic_fn, optimal_fn=a_star_inner_time):
    time = utils.convert_to_seconds(time)

    came_from, total_cost = optimal_fn(graph, start, goal, time, heuristic_fn)

    path = []
    current = came_from[goal]
    while current[0] != start:
        path.append((current[0], current[1],
                     utils.convert_to_time_string(current[2]),
                     utils.convert_to_time_string(current[3]), current[4]))
        current = came_from[current[0]]

    # dodajemy przystanek startowy
    path.append((current[0], current[1],
                 utils.convert_to_time_string(current[2]),
                 utils.convert_to_time_string(current[3]), current[4]))

    path.reverse()
    return total_cost, path, time


def execute_astar(graph, start, goal, time, option="t"):
    if option == "t":
        return a_star(graph, start, goal, time, heuristic_fn=utils.geo_distance, optimal_fn=a_star_inner_time)
    if option == "p":
        return a_star(graph, start, goal, time, heuristic_fn=utils.line_change_heuristic, optimal_fn=a_star_inner_line)
