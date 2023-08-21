"Python 3.10.8"
from dataclasses import dataclass
import numpy as np

from scaleup_sram import Scaleupsram
from dram_buffer import Drambuffer
from efficiency import Efficiency
from runtime import Runtime

#pylint: disable=E0402
from .._Dataclass.data_class import Systolic
from .._Dataclass.data_class import Scaleupformat
from .._Dataclass.data_class import Operand

class Scaleup:
    """
    Scaleup Simulation
    Needed information: systolic array size, input_operand, filter_operand, buffer size.
    """
    def __init__(self):
        self.scaleupsram = Scaleupsram()
        self.drambuffer = Drambuffer()
        self.efficiency = Efficiency()
        self.runtime = Runtime()

        self.scaleup_param = Scaleupformat(Systolic(0,0,0,0,0),
            Operand(np.zeros(1,1),0,0),(np.zeros(1,1),0,0),"WS")

    def scaleup(self, scaleup_param, stride):
        """Top function for scaleup simulation."""
        #Get Information from ScaleupInfo module: # of tiled dimension.
        self.scaleup_param.num_col_tiles, self.scaleup_param.num_row_tiles =\
            self.scaleupinfo(scaleup_param)

        #Get Memory Information
        sram_input, sram_filter, sram_output = self.scaleupsram.scaleupsram(scaleup_param, stride)
        dram_input, dram_filter, dram_output = self.drambuffer.dram_buffer(processor, info, input_operand, filter_operand, input_buf, filter_buf, dataflow)

        #Get mapping/computation efficiency/Runtime
        runtime, mac = self.runtime.get_runtime(processor, input_operand, filter_operand, dataflow)

        return [sram_input, sram_filter, sram_output, dram_input, dram_filter, dram_output, mac, runtime]


    def scaleupinfo(self, scaleup_params):
        """
        Get scaleup information form systolic array and operand matrix.
        Processor is entered in the form of lists: [sys_row, sys_col, ...]
        """
        sys_row, sys_col = scaleup_params.systolic.systolic_row, scaleup_params.systolic.systolic_col
        row, col = self._get_operand_dimensions(scaleup_params.input_operand,
            scaleup_params.filter_operand, scaleup_params.dataflow)
        num_row_tiles, num_col_tiles = self._get_num_tiles(sys_row, sys_col, row, col)

        return num_row_tiles, num_col_tiles

    #Dimension of operand matrix is different only with IS dataflow.
    def _get_operand_dimensions(self, input_operand, filter_operand, dataflow):
        """Get operand dimension."""
        if dataflow == "IS":
            return len(filter_operand), len(input_operand[0])
        else:
            return len(input_operand), len(filter_operand[0])

    #Calculate number of tiles
    def _get_num_tiles(self, sys_row, sys_col, row, col):
        """Get number of tiles that will be used."""
        num_row_tiles = int(np.ceil(row / sys_row))
        num_col_tiles = int(np.ceil(col / sys_col))

        return num_row_tiles, num_col_tiles
