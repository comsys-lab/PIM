"Python 3.11.5"
import numpy as np

from operand import Operand

class MakeFilter:
    """Make filter operand matrix and return"""
    def __init__(self):
        self.filter_operand = Operand(np.zeros((1,1)),0,0)

    #Input: list / Return: np.ndarray | int | int
    def make_filter_opreand(self, topo):
        """Make filter operand matrix"""
        row = topo[2] * topo[3] * topo[4]
        col = topo[5]

        filter_operand = \
            np.array([[str([i, j]) for j in range(col)] for i in range(row)], dtype='U20')

        return filter_operand, row, col

   #Input: list / Return: Operand
    def return_filter_matrix(self,topo):
        """Return filter operand matrix"""
        filter_operand, row, col = self.make_filter_opreand(topo)
        self.filter_operand.operand_matrix = filter_operand
        self.filter_operand.row = row
        self.filter_operand.col = col

        return self.filter_operand
