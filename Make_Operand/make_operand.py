"Python 3.11.5"
from .make_input import MakeInput
from .make_filter import MakeFilter
from .make_output import MakeOutput

class MakeOperand:
    """Make input and filter operand matrix and return"""
    def __init__(self):
        self.make_input = MakeInput()
        self.make_filter = MakeFilter()
        self.make_output = MakeOutput()

        self.input_operand = []
        self.filter_operand = []
        self.output_operand = []

    def return_operand_matrix(self, topo, dataflow):
        """Return input and filter operand matrix"""
        self.input_operand = self.make_input.return_input_operand(topo, dataflow)
        self.filter_operand = self.make_filter.return_filter_operand(topo)
        self.output_operand = self.make_output.return_output_operand(topo,dataflow)

        return self.input_operand, self.filter_operand, self.output_operand
