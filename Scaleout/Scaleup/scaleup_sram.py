"Python 3.11.5"
import numpy as np

from base_operation import Baseoperation

class Scaleupsram:
    """Get SRAM access count."""
    def __init__(self):
        self.base_operation = Baseoperation()

    #Input: scaleupformat | int / Return: list
    def scaleup_sram(self, scaleupformat, stride):
        """Get scaleup sram count. Divide case with stride."""
        dataflow = scaleupformat.dataflow
        if dataflow == "OS":
            return_sram_access = self.df_os(scaleupformat, stride)
        elif dataflow == "WS":
            return_sram_access = self.df_ws(scaleupformat, stride)
        elif dataflow == "IS":
            return_sram_access = self.df_is(scaleupformat, stride)

        return return_sram_access

    #Input: scaleupformat / Return: int | int
    def return_size_one(self, scaleupformat):
        """Return operand matrix size when stride is one."""
        input_size = scaleupformat.input_operand.shape[0] * scaleupformat.input_operand.shape[1]
        filter_size = scaleupformat.filter_operand.shape[0] * scaleupformat.filter_operand.shape[1]

        return input_size, filter_size

    #Input: scaleupformat / Return: int | int
    def return_size_over_one(self, scaleupformat):
        """Return operand matrix size when stride is over one."""
        input_size = self.base_operation.get_data_size_no_duplication(scaleupformat.input_operand.operand)
        _,filter_size = self.return_size_one(scaleupformat)

        return input_size, filter_size

    #Input: scaleupformat | int / Return: int | int
    def return_size(self, scaleupformat, stride):
        """Return input and filter matrix size."""
        if stride == 1:
            input_size, filter_size = self.return_size_one(scaleupformat)
        else:
            input_size, filter_size = self.return_size_over_one(scaleupformat)

        return input_size, filter_size

    #Input: scaleupformat | int / Return: list
    def df_os(self, scaleupformat, stride):
        """When dataflow is os"""
        input_size, filter_size = self.return_size(scaleupformat, stride)

        input_sram = int(np.ceil(scaleupformat.filter_operand.shape[1] / scaleupformat.systolic.shape[1])) * input_size
        filter_sram = int(np.ceil(scaleupformat.input_operand.shape[0] / scaleupformat.systolic.shape[0])) * filter_size
        output_sram = scaleupformat.input_operand.shape[0] * scaleupformat.filter_operand.shape[1]

        return_sram_access = [input_sram, filter_sram, output_sram]

        return return_sram_access

    #Input: scaleupformat | int / Return: list
    def df_ws(self, scaleupformat, stride):
        """When dataflow is ws"""
        input_size, filter_size = self.return_size(scaleupformat, stride)

        input_sram = int(np.ceil(scaleupformat.filter_operand.shape[1] / scaleupformat.systolic.shape[1])) * input_size
        filter_sram = filter_size
        output_sram = int(np.ceil(scaleupformat.input_operand.shape[1] / scaleupformat.systolic.shape[0])) \
            * scaleupformat.input_operand.shape[1] * scaleupformat.filter_operand.shape[1]

        return_sram_access = [input_sram, filter_sram, output_sram]

        return return_sram_access

    #Input: scaleupformat | int / Return: list
    def df_is(self, scaleupformat, stride):
        """When dataflow is is"""
        input_size, filter_size = self.return_size(scaleupformat, stride)

        input_sram = input_size
        filter_sram = int(np.ceil(scaleupformat.input_operand.shape[1] / scaleupformat.systolic.shape[1])) * filter_size
        output_sram = int(np.ceil(scaleupformat.filter_operand.shape[0] / scaleupformat.systolic.shape[0])) \
            * scaleupformat.input_operand.shape[1] * scaleupformat.filter_operand.shape[1]

        return_sram_access = [input_sram, filter_sram, output_sram]

        return return_sram_access
