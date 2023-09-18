"Python 3.11.5"
import numpy as np

from Make_operand.make_operand import MakeOperand

class Singlelayer:
    """. """
    def __init__(self):
        self.make_operand = MakeOperand()

    def single_layer(self, topo_one):
        input_operand, filter_operand = self.make_operand.return_operand_matrix(topo_one)

    def 