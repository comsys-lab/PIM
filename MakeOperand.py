from MakeOperand.MakeInput import MakeInput
from MakeOperand.MakeFilter import MakeFilter

class MakeOperand:
    def __init__(self):
        self.make_input = MakeInput()
        self.make_filter = MakeFilter()

    def return_operand(self, topo, dataflow):
        input_info, stride = self.make_input.return_input_operand(topo, dataflow)
        filter_operand = self.make_filter.return_filter_matrix(topo)

        if dataflow == "IS":
            # Handle the specific case for dataflow "IS" if needed
            pass

        return input_info, filter_operand, stride
