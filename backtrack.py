import numpy as np
from pqdict import minpq
import dijksta_func as df

def min_path(maps, nodes_list, graph_node, start, goal):
    distance, parent = df.dijkstra(graph_node, nodes_list, maps, block_nodes, start, goal)
    end = goal
    path = [end]
    while end != start:
        end = parent[end]
        path.append(end)
    path.reverse()
    return path