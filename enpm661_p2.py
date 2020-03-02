import numpy as np
from pqdict import minpq

nodes_list = {(0,0): False, (0,1): False, (0,2): False,
         (1,0): False, (1,1): False, (1,2): False,
         (2,0): False, (2,1): False, (2,2): False}

graph_node = {(0,0): {(0,1):1 ,(1,0):1 ,(1,1):np.round(np.sqrt(2),3)}, 
           (0,1): {(0,0):1, (0,2):1, (1,1):1, (1,0):np.round(np.sqrt(2),3), (1,2):np.round(np.sqrt(2),3)},
           (0,2): {(0,1):1, (1,1):np.round(np.sqrt(2),3), (1,2):1},
           (1,0): {(0,0):1, (0,1):np.round(np.sqrt(2),3), (1,1):1, (2,1):np.round(np.sqrt(2),3), (2,0):1},
           (1,1): {(0,0):np.round(np.sqrt(2),3), (0,1):1, (0,2):np.round(np.sqrt(2),3), (1,0):1, (1,2):1, (2,0):np.round(np.sqrt(2),3), (2,1):1, (2,2):np.round(np.sqrt(2),3)},
           (1,2): {(0,2):1, (2,2):1, (1,1):1, (0,1):np.round(np.sqrt(2),3), (2,1):np.round(np.sqrt(2),3)},
           (2,0): {(1,0):1, (2,1):1, (1.1):np.round(np.sqrt(2),3)},
           (2,1): {(2,0):1, (2,2):1, (1,1):1, (1,0):np.round(np.sqrt(2),3), (1,2):np.round(np.sqrt(2),3)},
           (2,2): {(1,2):1, (2,1):1, (1,1):np.round(np.sqrt(2),3)}}


# dijkstra funtion:

def dijkstra(graph_node, nodes_list, maps, block, start, goal=None):
    distance = {}
    parent = {}
    
    # making the obstacle nodes value = True
    # deleting the obstacle nodes from graph
    for b in block:
        for key in nodes_list:
            if b == key:
                nodes_list[key]=True
                del graph_node[key]
                #del graph_node[][key]
        
    
       
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
    

# function for backtrack
def min_path(maps, nodes_list, block, graph_node, start, goal):
    distance, parent = dijkstra(graph_node,nodes_list, maps, block, start, goal)
    end = goal
    path = [end]
    while end != start:
        end = parent[end]
        path.append(end)        
    path.reverse()
    return path

 # driver program 

start = (0,0)
goal = (2,2)
maps = np.matrix('0,0,0;0,1,0;0,0,0')
block= []

for i in range (0,3):
    for j in range (0,3):
        if maps[i,j] == 1:
            pos = (i,j)
            block.append(pos)
    
print(graph_node)        
print(min_path(maps, nodes_list, block, graph_node, start, goal))  