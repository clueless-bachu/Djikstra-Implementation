def block_nodes(maps, rows, cols):
    block = []
    for i in range(0, rows):
        for j in range(0, cols):
            if maps[i, j] == 1:
                pos = (i, j)
                block.append(pos)


    return block