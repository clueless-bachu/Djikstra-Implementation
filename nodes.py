
def nodes_list(maps, blocked_nodes):

    nodes = []
    nodes_list = {}
    for rows in len(maps):
        for cols in len(maps):
            pos = (rows,cols)
            nodes.append(pos)

    # setting value of all nodes as False
    for i in range(0, len(nodes)):
        nodes_list[nodes[i]] = False

    # deleting the obstacle nodes from graph
    for b in blocked_nodes:
        for key in nodes_list:
            if b == key:
                del nodes_list[key]

    # updating nodes
    for b in blocked_nodes:
        for n in nodes:
            if b == n:
                nodes.pop(n)

    return nodes_list, nodes


        # nodes_listnodes_list = {(0, 0): False, (0, 1): False, (0, 2): False,
        #       (1, 0): False, (1, 1): False, (1, 2): False,
        #       (2, 0): False, (2, 1): False, (2, 2): False}



def graph_node(maps, nodes):

    graph_node = {}
    for key in nodes:
        graph_node.setdefault(key, {'cost': None})




    return graph_node


cost = {'up': 1, 'down': 1, 'right': 1, 'left': 1,
            'up-left': np.round(np.sqrt(2),3), 'up-right': np.round(np.sqrt(2),3),
            'down-left': np.round(np.sqrt(2),3), 'down-right': np.round(np.sqrt(2),3)}   

actions = {'up': (-1,0), 'down': (1,0), 'right': (0,1), 'left': (-1,0),
            'up-left': (-1,-1), 'up-right': (-1,1), 'down-left': (1,-1), 'down-right': (1,1)}
