"Python 3.11.5"
import numpy as np

from scaleup_sram import Scaleupsram
from scaleup_runtime import Scaleupruntime

from scaleup_class import Systolic


class Scaleup:
    """Scaleup simulation"""
    def __init__(self):
        self.scaleupsram = Scaleupsram()
        self.scaleupruntime = Scaleupruntime()

    def scaleup(self, scaleup, operand, stride):
        """With scaleup(format), operand and stride get information from scaleup"""

        #Get Information from ScaleupInfo module: # of tiled dimension.
        scaleupinfo = self.scaleup_info(scaleup, operand)

        #Get runtime with scaleup information and operand information.
        runtime = self.scaleupruntime.get_runtime(scaleup, operand)

        #Get Memory Information
        sram_access = self.scaleupsram.scaleup_sram(scaleup, operand, stride)
        dram_access, stall = 0, 0

        return sram_access, dram_access, runtime, stall

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
        num_tiles_row = int(np.ceil(row / scaleup.systolic.row ))
        num_tiles_col = int(np.ceil(col / scaleup.systolc.col ))
        scaleupinfo = [num_tiles_row, num_tiles_col]
        return scaleupinfo

