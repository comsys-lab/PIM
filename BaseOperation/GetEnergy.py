import configparser as cp

class GetEnergy:
    def __init__(self):
        self.MAC_Parameters = []
        self.NPU_Parameters = []
        self.PIM_Parameters = []

    def GetEnergy(self, path):
        config = cp.ConfigParser()
        config.read(path)

        #Enter the MAC_Parameters
        section = 'MAC_Parameters'
        self.MAC_random = config.getfloat(section, 'MAC_random')
        self.MAC_reused = config.getfloat(section, 'MAC_reused')
        self.MAC_gated = config.getfloat(section, 'MAC_gated')
        self.MAC_idle = config.getfloat(section, 'MAC_idle')

        #Enter the NPU_Parameters
        section = 'NPU_Parameters'
        self.NPU_Input_DRAM_Access = config.getfloat(section, 'NPU_Input_DRAM_Access')
        self.NPU_Filter_DRAM_Access = config.getfloat(section, 'NPU_Filter_DRAM_Access')
        self.NPU_Output_DRAM_Access = config.getfloat(section, 'NPU_Output_DRAM_Access')
        self.NPU_Input_SRAM_Access = config.getfloat(section, 'NPU_Input_SRAM_Access')
        self.NPU_Filter_SRAM_Access = config.getfloat(section, 'NPU_Filter_SRAM_Access')
        self.NPU_Output_SRAM_Access = config.getfloat(section, 'NPU_Output_SRAM_Access')

        #Enter the PIM_Parameters
        section = 'PIM_Parameters'
        self.PIM_Input_DRAM_Access = config.getfloat(section, 'PIM_Input_DRAM_Access')
        self.PIM_Filter_DRAM_Access = config.getfloat(section, 'PIM_Filter_DRAM_Access')
        self.PIM_Output_DRAM_Access = config.getfloat(section, 'PIM_Output_DRAM_Access')
        self.PIM_Input_SRAM_Access = config.getfloat(section, 'PIM_Input_SRAM_Access')
        self.PIM_Filter_SRAM_Access = config.getfloat(section, 'PIM_Filter_SRAM_Access')
        self.PIM_Output_SRAM_Access = config.getfloat(section, 'PIM_Output_SRAM_Access')
        
    def return_energy_parameters(self):
        self.MAC_Parameters = [self.MAC_random, self.MAC_reused, self.MAC_gated, self.MAC_idle]
        self.NPU_Parameters = [self.NPU_Input_DRAM_Access, self.NPU_Filter_DRAM_Access, self.NPU_Output_DRAM_Access,\
                               self.NPU_Input_SRAM_Access, self.NPU_Filter_SRAM_Access, self.NPU_Output_SRAM_Access]
        self.PIM_Parameters = [self.PIM_Input_DRAM_Access, self.PIM_Filter_DRAM_Access, self.PIM_Output_DRAM_Access, \
                               self.PIM_Input_SRAM_Access, self.PIM_Filter_SRAM_Access, self.PIM_Output_SRAM_Access]
        
        return self.MAC_Parameters, self.NPU_Parameters, self.PIM_Parameters