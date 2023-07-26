from Base.ScaleupInfo import ScaleupInfo
from scaleup.ScaleupSRAM import ScaleupSRAM
from scaleup.DramBuffer import DramBuffer
from scaleup.Efficiency import Efficiency
from scaleup.Runtime import Runtime


class ScaleupBWIdeal:
    def __init__(self):
        self.ScaleupInfo = ScaleupInfo()
        self.ScaleupSRAM = ScaleupSRAM()
        self.DramBuffer = DramBuffer()
        self.Efficiency = Efficiency()
        self.Runtime = Runtime()

    def scaleup_bw_ideal(self, processor, input_operand, filter_operand, input_buf, filter_buf, dataflow, stride):
        #Get Information
        info = self.ScaleupInfo.scaleup_get_info(processor, input_operand, filter_operand, dataflow)
        
        #Get Memory Information
        sram_input, sram_filter, sram_output = self.ScaleupSRAM.scaleup_sram(info, input_operand, filter_operand, dataflow, stride)
        dram_input, dram_filter, dram_output = self.DramBuffer.dram_buffer(processor, info, input_operand, filter_operand, input_buf, filter_buf, dataflow)
        
        #Get mapping/computation efficiency/Runtime
        runtime, MAC = self.Runtime.get_runtime(processor, input_operand, filter_operand, dataflow)
        
        return [sram_input, sram_filter, sram_output, dram_input, dram_filter, dram_output, MAC, runtime]