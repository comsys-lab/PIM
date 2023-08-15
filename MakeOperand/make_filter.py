"Python 3.10.8"
from dataclasses import dataclass

import numpy as np

@dataclass
class Filteroperand:
    """Class for filter operand matrix"""
    filter_operand: np.ndarray
    filter_row: int
    filter_col: int

class MakeFilter:
    """Make filter operand matrix and return"""
    def __init__(self):
        self.filter_operand = Filteroperand(np.zeros((1,1)),0,0)

    def make_filter_opreand(self, topo):
        """Return filter operand matrix"""
        row = topo[2] * topo[3] * topo[4]
        col = topo[5]

        filter_operand = \
            np.array([[str([i, j]) for j in range(col)] for i in range(row)], dtype='U20')

        return filter_operand, row, col

    def return_filter_matrix(self,topo):
        """."""
        filter_operand, row, col = self.make_filter_opreand(topo)
        self.filter_operand.filter_operand = filter_operand
        self.filter_operand.filter_row = row
        self.filter_operand.filter_col = col

        return self.filter_operand
