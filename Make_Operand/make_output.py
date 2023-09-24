"Python 3.11.5"
import numpy as np

from .make_input import MakeInput

class MakeOutput:
    """Make output operand matrix and return"""
    def __init__(self):
        self.output_operand = np.zeros((1,1), dtype='U20')
        self.make_input = MakeInput()

    def make_output_matrix(self, topo):
        output_row, output_col = self.make_input.make_output(topo)
        Nofmap = output_row * output_col
        Nfilter = topo[5]

        output_operand = \
            np.array([[str([i, j]) for j in range(Nfilter)] for i in range(Nofmap)], dtype='U20')

        return output_operand

    def return_output_operand(self, topo, dataflow):
        """Return output operand matrix"""
        output_operand = self.make_output_matrix(topo)
        if dataflow == "IS":
            output_operand = np.transpose(output_operand)
        self.output_operand = output_operand

        return self.output_operand