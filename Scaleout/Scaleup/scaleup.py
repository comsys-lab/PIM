"Python 3.11.5"
import numpy as np

from scaleup_sram import Scaleupsram
from dram_buffer import Drambuffer
from 


from scaleup_class import Systolic
from scaleup_class import Scaleup

class Scaleup:
    """Scaleup simulation"""
    def __init__(self):
        self.scaleupsram = Scaleupsram()
        self.drambuffer = Drambuffer()
        self.runtime = Runtime()

        self.scaleup = []
        self.scaleup_param = Scaleupformat(Systolic(0,0,0,0,0),
            Operand(np.zeros(1,1),0,0),(np.zeros(1,1),0,0),"WS")

    def scaleup(self, scaleupformat, stride):
        """With scaleupformat and stride, get information from scaleup"""

        #Get Information from ScaleupInfo module: # of tiled dimension.
        num_tiles_row, num_tiles_col = self.get_num_tiles(scaleup, operand)

        #Get Memory Information
        sram_access = self.scaleupsram.scaleupsram(scaleupformat, stride)
        dram_access = 0

        runtime = 0

        return 1

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
    def get_num_tiles(self, scaleupformat):
        """Get number of tiles that will be used."""
        row, col = self.get_operand_dimensions(scaleupformat)
        num_tiles_row = int(np.ceil(row/ scaleupformat.systolic.shape[0] ))
        num_tiles_col = int(np.ceil(col /scaleupformat.systolc.shape[1]))

        return num_tiles_row, num_tiles_col

