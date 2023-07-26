import numpy as np

class MakeFilter:
    def return_filter_matrix(self, topo):
        row = topo[2] * topo[3] * topo[4]
        col = topo[5]

        filter_operand = np.array([[str([i, j]) for j in range(col)] for i in range(row)], dtype='U20')

        return filter_operand