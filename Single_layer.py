"Python 3.11.5"

from Make_operand.make_operand import MakeOperand
from Scaleout.scaleout import Scaleout

class Singlelayer:
    """. """
    def __init__(self):
        self.make_operand = MakeOperand()
        self.scaleout = Scaleout()

    def single_layer(self, topo_one, dataflow):
        """Get topology from self.topo, return simulation results."""
        input_operand, filter_operand = self.make_operand.return_operand_matrix(topo_one, dataflow)
        self.scaleout.scaleout(input_operand, filter_operand)

    def return_information(self, topo_one):
        pass


