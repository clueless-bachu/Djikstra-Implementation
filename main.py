import numpy as np
from pqdict import minpq
import convert as c
import block as b
import backtrack as bk
import nodes as nd

print("Generating map")
m = int(input('Enter the no of order of matrix'))
# n = int(input('Enter the no of columns of matrix'))
maps = np.random.randint(0, 2, (m, m))
print(maps)
print(len(maps))
s_n = input('Enter the start node with space')
start = c.convert(s_n)
g_n = input('Enter the goal node with space')
goal = c.convert(g_n)

block_nodes = b.block(maps, m, n)
nodes_list, nodes = nd.nodes_list(maps, block_nodes)
graph_node = nd.graph_node(maps, nodes)


print(bk.min_path(maps, nodes_list, graph_node, start, goal))