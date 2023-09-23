"Python 3.11.5"
import numpy as np

from .base_operation import Baseoperation

class Scaleupsram:
    """Get SRAM access count."""
    def __init__(self):
        self.base_operation = Baseoperation()

    #Input: scaleupformat | int / Return: list
    def scaleup_sram(self, scaleup, operand, stride):
        """Get scaleup sram count. Divide case with stride."""
        dataflow = scaleup.others.dataflow
        if dataflow == "OS":
            return_sram_access = self.df_os(scaleup, operand, stride)
        elif dataflow == "WS":
            return_sram_access = self.df_ws(scaleup, operand, stride)
        elif dataflow == "IS":
            return_sram_access = self.df_is(scaleup, operand, stride)

        return return_sram_access

    #Input: scaleupformat / Return: int | int
    def return_size_one(self, operand):
        """Return operand matrix size when stride is one."""
        input_size = operand.input_operand.shape[0] * operand.input_operand.shape[1]
        filter_size = operand.filter_operand.shape[0] * operand.filter_operand.shape[1]

        return input_size, filter_size

    #Input: scaleupformat / Return: int | int
    def return_size_over_one(self, operand):
        """Return operand matrix size when stride is over one."""
        input_size = self.base_operation.get_data_size_no_duplication(operand.input_operand)
        _,filter_size = self.return_size_one(operand.filter_operand)

        return input_size, filter_size

    #Input: scaleupformat | int / Return: int | int
    def return_size(self, operand, stride):
        """Return input and filter matrix size."""
        if stride == 1:
            input_size, filter_size = self.return_size_one(operand)
        else:
            input_size, filter_size = self.return_size_over_one(operand)

        return input_size, filter_size

    #-------------------------------------------------------------------------

    #Input: scaleupformat | int / Return: list
    def df_os(self, scaleup, operand, stride):
        """When dataflow is os"""
        input_size, filter_size = self.return_size(operand, stride)

        input_sram = int(np.ceil(operand.filter_operand.shape[1] / scaleup.systolic.col)) * input_size
        filter_sram = int(np.ceil(operand.input_operand.shape[0] / scaleup.systolic.row)) * filter_size
        output_sram = operand.input_operand.shape[0] * operand.filter_operand.shape[1]

        return_sram_access = [input_sram, filter_sram, output_sram]

        return return_sram_access

    #Input: scaleupformat | int / Return: list
    def df_ws(self, scaleup, operand, stride):
        """When dataflow is ws"""
        input_size, filter_size = self.return_size(operand, stride)

        input_sram = int(np.ceil(operand.filter_operand.shape[1] / scaleup.systolic.col)) * input_size
        filter_sram = filter_size
        output_sram = int(np.ceil(operand.input_operand.shape[1] / scaleup.systolic.row)) \
            * operand.input_operand.shape[1] * operand.filter_operand.shape[1]

        return_sram_access = [input_sram, filter_sram, output_sram]

        return return_sram_access

    #Input: scaleupformat | int / Return: list
    def df_is(self, scaleup, operand, stride):
        """When dataflow is is"""
        input_size, filter_size = self.return_size(operand, stride)

        input_sram = input_size
        filter_sram = int(np.ceil(operand.input_operand.shape[1] / scaleup.systolic.col)) * filter_size
        output_sram = int(np.ceil(operand.filter_operand.shape[0] / scaleup.systolic.row)) \
            * operand.input_operand.shape[1] * operand.filter_operand.shape[1]

        return_sram_access = [input_sram, filter_sram, output_sram]

        return return_sram_access
