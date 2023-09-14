"Python 3.11.2"
import numpy as np

class Runtime:
    """
    Runtime from scalesim
    """
    def get_runtime(self, processor, input_operand, filter_operand, dataflow):
        """Runtime division with dataflow of each simulation."""
        if dataflow == "OS":
            runtime, MAC = self.OS(processor, input_operand, filter_operand)
        elif dataflow == "WS":
            runtime, MAC = self.WS(processor, input_operand, filter_operand)
        elif dataflow == "IS":
            runtime, MAC = 0,0

        return runtime, MAC

    def _get_operand_dimensions(self, input_operand, filter_operand, dataflow):
        """Return operand dimensions from each dataflow."""
        if dataflow == "IS":
            pass
        elif (dataflow == "OS") or (dataflow == "WS"):
            SR = len(input_operand)
            SC = len(filter_operand[0])
            T = len(input_operand[0])

        return SR,SC,T

    def OS(self, processor, input_operand, filter_operand):
        """Return OS dataflow runtime."""
        SR,SC,T = self._get_operand_dimensions(input_operand, filter_operand, "OS")
        row_q = SR // processor[0]
        col_q = SC // processor[1]

        row_rest = (SR % processor[0])
        col_rest = (SC % processor[1])

        row_flag = (SR % processor[0]) != 0
        col_flag = (SC % processor[1]) != 0

        #CASE1
        runtime1 = T + processor[0] + (processor[0] + processor[1] - 2)
        #CASE2
        runtime2 = T + processor[0] + (row_rest + processor[1] - 2)
        #CASE3
        runtime3 = T + processor[0] + (processor[0] + col_rest - 2)
        #CASE4
        runtime4 = T + processor[0] + (row_rest + col_rest - 2)

        runtime = runtime1 * row_q * col_q + runtime2 * row_flag * col_q + runtime3 * row_q * col_flag + runtime4 * row_flag * col_flag
        MAC = SR * SC * T
        return runtime, MAC

    def WS(self, processor, input_operand, filter_operand):
        """Return WS dataflow runtime."""
        SR,SC,T = self._get_operand_dimensions(input_operand, filter_operand, "WS")
        row_q = SR // processor[0]
        col_q = SC // processor[1]

        row_rest = (SR % processor[0])
        col_rest = (SC % processor[1])

        row_flag = (SR % processor[0]) != 0
        col_flag = (SC % processor[1]) != 0

        #CASE1
        runtime1 = T + processor[0] - 1 + (processor[0] + processor[1] - 1)
        #CASE2
        runtime2 = T + processor[0] - 1 + (row_rest + processor[1] - 1)
        #CASE3
        runtime3 = T + processor[0] - 1 + (processor[0] + col_rest- 1)
        #CASE4
        runtime4 = T + processor[0] - 1 + (row_rest + col_rest - 1)

        runtime = runtime1 * row_q * col_q + runtime2 * row_flag * col_q + runtime3 * row_q * col_flag + runtime4 * row_flag * col_flag

        MAC = SR * SC * T
        return runtime, MAC

    def IS(self, processor, input_operand, filter_operand):
        """Return IS dataflow runtime."""
        SR,SC,T = self._get_operand_dimensions(input_operand, filter_operand, "IS")
        row_q = SR // processor[0]
        col_q = SC // processor[1]

        row_rest = (SR % processor[0])
        col_rest = (SC % processor[1])

        row_flag = (SR % processor[0]) != 0
        col_flag = (SC % processor[1]) != 0

        #CASE1
        runtime  = T + processor[0] - 1 +