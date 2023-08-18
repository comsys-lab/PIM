
"Python 3.10.8"
from make_input import MakeInput
from make_filter import MakeFilter

class MakeOperand:
    """Make input and filter operand matrix and return"""
    def __init__(self):
        self.make_input = MakeInput()
        self.make_filter = MakeFilter()

        self.input_operand = []
        self.filter_operand = []

    def return_operand_matrice(self, topo, dataflow):
        """Return input and filter operand matrix"""
        self.input_operand = self.make_input.return_input_operand(topo, dataflow)
        self.filter_operand = self.make_filter.return_filter_matrix(topo)

        return self.input_operand, self.filter_operand
