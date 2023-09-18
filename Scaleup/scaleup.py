"Python 3.11.5"
import numpy as np

from scaleup_sram import Scaleupsram
from dram_buffer import Drambuffer

from scaleup_runtime import Runtime

from scaleup_class import Systolic
from scaleup_class import Scaleupformat
from scaleup_class import Operand

class Scaleup:
    """Scaleup simulation"""
    def __init__(self):
        self.scaleupsram = Scaleupsram()
        self.drambuffer = Drambuffer()
        self.runtime = Runtime()

        self.scaleup_param = Scaleupformat(Systolic(0,0,0,0,0),
            Operand(np.zeros(1,1),0,0),(np.zeros(1,1),0,0),"WS")

    def scaleup(self, scaleupformat, stride):
        """With scaleupformat and stride, get information from scaleup"""

        #Get Information from ScaleupInfo module: # of tiled dimension.
        num_tiles_row, num_tiles_col = self.get_num_tiles(scaleupformat)

        #Get Memory Information
        sram_access = self.scaleupsram.scaleupsram(scaleupformat, stride)
        dram_access = self.drambuffer.dram_buffer(processor, info, input_operand, filter_operand, input_buf, filter_buf, dataflow)


        runtime, mac = self.runtime.get_runtime(processor, input_operand, filter_operand, dataflow)

        return 1

    #Input: scaleupformat / Return: int | int
    def get_operand_dimensions(self, scaleupformat):
        """
        Get operand dimension.
        Dimension of operand matrix is different only with IS dataflow.
        """
        if scaleupformat.dataflow == "IS":
            return scaleupformat.filter_operand.row, scaleupformat.input_operand.col
        else:
            return scaleupformat.input_operand.row, scaleupformat.filter_operand.col

    #Input: scaleupformat / Return: int | int
    def get_num_tiles(self, scaleupformat):
        """Get number of tiles that will be used."""
        row, col = self._get_operand_dimensions(scaleupformat)
        num_tiles_row = int(np.ceil(row/ scaleupformat.systolic.row ))
        num_tiles_col = int(np.ceil(col /scaleupformat.systolc.col))

        return num_tiles_row, num_tiles_col

