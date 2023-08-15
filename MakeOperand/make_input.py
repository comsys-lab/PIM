"Python 3.10.8"
from dataclasses import dataclass
import numpy as np

@dataclass
class Inputoperand:
    """Class for input operand matrix"""
    input_operand: np.ndarray
    input_row: int
    input_col: int

class MakeInput:
    """Make input operand matrix and return"""
    def __init__(self):
        self.input_operand = Inputoperand(np.zeros((1,1)),0,0)

    def make_input_matrix(self, topo):
        """Make input matrix"""
        input_matrix = np.array([[[[i, j, k] for k in range(topo[1])] \
                                  for j in range(topo[0])] for i in range(topo[4])])

        return input_matrix

    def make_output(self, topo):
        """Return output row and column."""
        o_row = int(np.ceil((topo[0] - topo[2] + topo[6]) / topo[6]))
        o_col = int(np.ceil((topo[1] - topo[3] + topo[6]) / topo[6]))

        return o_row, o_col

    def make_input_operand_os(self, topo):
        """Make input operand matrix."""
        input_matrix = self.make_input_matrix(topo)
        o_row, o_col = self.make_output(topo)
        result = []

        for x in range(o_row):
            for y in range(o_col):
                temp = []
                for i in range(topo[4]):
                    for j in range(topo[2]):
                        for k in range(topo[3]):
                            row = x * topo[6] + j
                            col = y * topo[6] + k
                            if row < topo[0] and col < topo[1]:
                                temp.append(str(input_matrix[i, row, col]))
                            else:
                                temp.append("[-1,-1,-1]")
                result.append(temp)
        result = np.array(result, dtype='U20')

        return result

    def make_input_operand_ws_is(self, topo):
        """Make input operand matrix for WS and IS dataflow."""
        temp = self.make_input_operand_os(topo)
        result = np.transpose(temp)

        return result

    def return_input_operand(self, topo, dataflow):
        """Return input operand matrix."""
        if dataflow == "OS":
            self.input_operand = self.make_input_operand_os(topo)
        else:
            self.input_operand = self.make_input_operand_ws_is(topo)

        return self.input_operand