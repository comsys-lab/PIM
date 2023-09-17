"Python 3.11.5"
import numpy as np

from base_operation import Baseoperation

class Scaleup_dram:
    """Get DRAM access count."""
    def __init__(self):
        self.base_operation = Baseoperation()

    def scaleup_dram(self, scaleupformat):
        """."""
        dataflow = scaleupformat.dataflow
        if dataflow == "OS":
            return_dram_access = self.df_os(scaleupformat)
        elif dataflow == "WS":
            return_dram_access = self.df_ws(scaleupformat)
        elif dataflow == "IS":
            return_dram_access = self.df_is(scaleupformat)

        return return_dram_access
    #what about bandwidth and latency?

    def df_os(self, scaleupformat):
        systolic = scaleupformat.systolic
        input_operand = scaleupformat.input_operand
        filter_operand = scaleupformat.filter_operand

        input_access = 0
        filter_access = 0
        output_access = scaleupformat.input_operand.row * scaleupformat.filter_operand.col

        if input_operand.row % systolic.row != 0:
            pass

    def df_ws(self):
        pass

    def df_is(self):
        pass