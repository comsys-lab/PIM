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

        self.scaleup_param = Scaleupformat(Systolic(0,0,0,0,0),0,0,np.zeros(1,1),np.zeros(1,1),"WS")

    def scaleup(self, params, stride):
        """Top function for scaleup simulation."""
        #Get Information from ScaleupInfo module: # of tiled dimension.
        self.scaleup_param.num_col_tiles, self.scaleup_param.num_row_tiles =\
            self.scaleupinfo(processor, input_operand, filter_operand, dataflow)

        #Get Memory Information
        sram_input, sram_filter, sram_output = self.scaleupsram.scaleupsram(info, input_operand, filter_operand, dataflow, stride)
        dram_input, dram_filter, dram_output = self.drambuffer.dram_buffer(processor, info, input_operand, filter_operand, input_buf, filter_buf, dataflow)

        #Get mapping/computation efficiency/Runtime
        runtime, mac = self.runtime.get_runtime(processor, input_operand, filter_operand, dataflow)

        return [sram_input, sram_filter, sram_output, dram_input, dram_filter, dram_output, mac, runtime]


    def scaleupinfo(self, systolic, input_operand, filter_operand, dataflow):
        """
        Get scaleup information from input and filter matrix.
        Dimension of operand matrix is different depending on the dataflow.
        Get scaleup information form processor and operand matrix.
        Processor is entered in the form of lists: [sys_row, sys_col, pod_dim_row, pod_dim_col]
        In scaleup case, simulator only needs the dimension of systolic array: [sys_row, syscol]
        """
        sys_row, sys_col = systolic.systolic_row, systolic.systolic_col
        row, col = self._get_operand_dimensions(input_operand, filter_operand, dataflow)
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
        num_row_tiles = int(np.ceil(row / sys_row))
        num_col_tiles = int(np.ceil(col / sys_col))

        return num_row_tiles, num_col_tiles
