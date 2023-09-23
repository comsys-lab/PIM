topo = [[1,2,3],[4,5,6],[1,2,3],[1,2,3],[1,2,3],[1,2,3]]

def check_topology(topology):
    """Remove duplication in layer, and check stride."""
    check_layer = []
    for layer in topology:
        if layer not in check_layer:
            check_layer.append(layer)

    new_topo = []
    for i in range(len(check_layer)):
        new_topo.append([0,[]])

    for layer in topology:
        index = check_layer.index(layer)
        new_topo[index][0] += 1
        print(new_topo[index][1] == [])
        if new_topo[index][1] == []:
            new_topo[index][1] = layer

    return new_topo

print(check_topology(topo))

length = len(topo)
for i in range(length):
    pass

        #CASE1
        runtime1 = (t + scaleup.systolic.row + (scaleup.systolic.row + scaleup.systolic.col - 2)) * row_q * col_q
        #CASE2
        runtime2 = (t + scaleup.systolic.row + (row_rest + scaleup.systolic.col - 2)) * row_flag * col_q
        #CASE3
        runtime3 = (t + scaleup.systolic.row + (scaleup.systolic.row + col_rest - 2)) * row_q * col_flag
        #CASE4
        runtime4 = (t + scaleup.systolic.row + (row_rest + col_rest - 2)) * row_flag * col_flag