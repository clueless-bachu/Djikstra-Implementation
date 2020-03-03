from pqdict import minpq

def dijkstra(graph_node, nodes_list, maps, start, goal=None):
    distance = {}
    parent = {}

    priority_queue = minpq()
    # Setting initial values to all the nodes
    for node in graph_node:
        if node == start:
            priority_queue[node] = 0
        else:
            priority_queue[node] = float('inf')

    # updating distance of each node
    for node, min_distance in priority_queue.popitems():
        distance[node] = min_distance
        if node == goal:
            break

        # note of parent node
        for neighbor in graph_node[node]:
            if neighbor in priority_queue:
                new_cost = distance[node] + graph_node[node][neighbor]
                if new_cost < priority_queue[neighbor]:
                    priority_queue[neighbor] = new_cost
                    parent[neighbor] = node

    return distance, parent
