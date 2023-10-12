"Python 3.11.5"
import numpy as np

class MakeFilter:
    """Make filter operand matrix and return"""
    def __init__(self):
        self.filter_operand = np.zeros((1,1), dtype='U20')

    #Input: list / Return: np.ndarray | int | int
    def make_filter_opreand(self, topo):
        """Make filter operand matrix"""
        row = topo[2] * topo[3] * topo[4]
        col = topo[5]
        maximum = len(str(row))

        filter_operand = \
            np.array([[i*pow(10,maximum)+j for j in range(col)] for i in range(row)], dtype = np.int32)

        return filter_operand

    #Input: list / Return: Operand
    def return_filter_operand(self,topo):
        """Return filter operand matrix"""
        filter_operand = self.make_filter_opreand(topo)
        self.filter_operand = filter_operand

        return self.filter_operand
