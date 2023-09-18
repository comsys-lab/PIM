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

    def scaleup_dram(self, scaleupformat, stride):
        """Get scaleup dram count. Divide case with stride."""
        dataflow = scaleupformat.dataflow
        if dataflow == "OS":
            return_dram_access = self.df_os(scaleupformat, stride)
        elif dataflow == "WS":
            return_dram_access = self.df_ws(scaleupformat, stride)
        elif dataflow == "IS":
            return_dram_access = self.df_is(scaleupformat, stride)

        return return_dram_access

    def make_input_1d(self, input_operand):
        pass

    def make_filter_1d(self, filter_operand):
        pass

    def _df_os(sefl, scaleupformat, stride):
        """."""
        if stride == 1:
            pass
        else:
            pass


    def df_os(self, scaleupformat, stride):
        """When dataflow is os"""
        #Divide case with stride.
        if stride == 1:
            pass
        else:
            pass

        systolic = scaleupformat.systolic
        input_operand = scaleupformat.input_operand
        filter_operand = scaleupformat.filter_operand

        input_access = 0
        filter_access = 0
        output_access = scaleupformat.input_operand.row * scaleupformat.filter_operand.col

        if input_operand.row % systolic.row != 0:
            pass

    def df_ws(self, scaleupformat, stride):
        """When dataflow is ws."""
        if stride == 1:
            pass
        else:
            pass

        return 1

    def df_is(self, scaleupformat, stride):
        """When dataflow is is."""
        if stride == 1:
            pass
        else:
            pass

        return 1

    def skew_input(self, input_operand):
        pass

    def skew_filter(self, filter_operand):
        pass