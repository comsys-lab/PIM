from ScaleupInfo import ScaleupInfo
from ScaleupSRAM import ScaleupSRAM
from DramBuffer import DramBuffer
from Efficiency import Efficiency
from Runtime import Runtime


class ScaleupBWIdeal:
    def __init__(self):
        self.ScaleupInfo = ScaleupInfo()

        self.ScaleupSRAM = ScaleupSRAM()
        self.DramBuffer = DramBuffer()
        self.Efficiency = Efficiency()
        self.Runtime = Runtime()

    def ScaleupBWIdeal(self, processor, input_operand, filter_operand, input_buf, filter_buf, dataflow, stride):
        #Get Information from ScaleupInfo module: # of tiled dimension.
        num_row_tiles, num_col_tiles = self.ScaleupInfo.scaleup_get_info(processor, input_operand, filter_operand, dataflow)

        #Get Memory Information
        sram_input, sram_filter, sram_output = self.ScaleupSRAM.scaleup_sram(info, input_operand, filter_operand, dataflow, stride)
        dram_input, dram_filter, dram_output = self.DramBuffer.dram_buffer(processor, info, input_operand, filter_operand, input_buf, filter_buf, dataflow)

        #Get mapping/computation efficiency/Runtime
        runtime, MAC = self.Runtime.get_runtime(processor, input_operand, filter_operand, dataflow)

        return [sram_input, sram_filter, sram_output, dram_input, dram_filter, dram_output, MAC, runtime]