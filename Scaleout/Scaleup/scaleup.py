"Python 3.11.5"
import numpy as np

from .scaleup_sram import Scaleupsram
from .scaleup_dram import Scaleupdram
from .scaleup_runtime import Scaleupruntime

from .base_class import Results

class ScaleUp:
    """Scaleup simulation"""
    def __init__(self):
        self.scaleupsram = Scaleupsram()
        self.scaleupdram = Scaleupdram()
        self.scaleupruntime = Scaleupruntime()

    def scale_up(self, scaleup, operand, stride):
        """With scaleup(format), operand and stride get information from scaleup"""

        #Get Information from ScaleupInfo module: # of tiled dimension.
        scaleupinfo = self.scaleup_info(scaleup, operand)

        #Get Memory Information
        input_sram, filter_sram, output_sram = self.scaleupsram.scaleup_sram(scaleup, operand, stride)
        input_dram, filter_dram, output_dram, stall = self.scaleupdram.scaleup_dram(scaleup, operand, scaleupinfo)

        #Get runtime with scaleup information and operand information.
        runtime = self.scaleupruntime.get_runtime(scaleup, operand)
        runtime += stall

        result_list = [input_sram, filter_sram, output_sram, input_dram, filter_dram, output_dram, runtime]
        results = self.results(result_list)

        return results

    def scaleup_mobile(self, scaleup, operand):
        """Scaleup function for mobile form factor"""
        runtime = self.scaleupruntime.get_runtime(scaleup, operand)

        return runtime

    #Input: scaleupformat / Return: int | int
    def get_operand_dimensions(self, scaleup, operand):
        """
        Get operand dimension.
        Dimension of operand matrix is different only with IS dataflow.
        """
        if scaleup.others.dataflow == "IS":
            return operand.filter_operand.shape[0], operand.input_operand.shape[1]
        else:
            return operand.input_operand.shape[0], operand.filter_operand.shape[1]

    #Input: scaleupformat / Return: int | int
    def scaleup_info(self, scaleup, operand):
        """Get number of tiles that will be used."""
        row, col = self.get_operand_dimensions(scaleup, operand)

        full_row = scaleup.systolic.row
        full_col = scaleup.systolic.col
        rest_row = row % scaleup.systolic.row
        rest_col = col % scaleup.systolic.col

        num_row = int(np.ceil(row / scaleup.systolic.row))
        num_col = int(np.ceil(col / scaleup.systolic.col))

        scaleupinfo = [[num_row,num_col],[full_row, rest_row],[full_col, rest_col]]

        return scaleupinfo

    def results(self, result_list):
        """Collect results from scaleup"""
        results = Results(0,0,0,0,0,0,0,0)

        results.input_sram = result_list[0]
        results.filter_sram = result_list[1]
        results.output_sram = result_list[2]
        results.input_dram = result_list[3]
        results.filter_dram = result_list[4]
        results.output_dram = result_list[5]
        results.runtime = result_list[6]

        return results
