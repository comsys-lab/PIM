"Python 3.11.5"
import configparser as cp

from .get_class import MACenergy
from .get_class import Energy

class GetEnergy:
    """Get energy parameters from configuration file (.cfg)."""
    def __init__(self):
        self.mac_energy = MACenergy(0,0,0,0)
        self.npu_energy = Energy(0,0,0,0,0,0)
        self.pim_energy = Energy(0,0,0,0,0,0)

    #Input: str | str | str
    def get_energy(self, path, npu_df, pim_df):
        """Get energy parameters from configuration file path."""
        config = cp.ConfigParser()
        config.read(path)

        #Enter the mac_Parameters
        section = 'mac_parameters'

        self.mac_energy.mac_random = config.getfloat(section, 'mac_random')
        self.mac_energy.mac_reused = config.getfloat(section, 'mac_reused')
        self.mac_energy.mac_gated = config.getfloat(section, 'mac_gated')
        self.mac_energy.mac_idle = config.getfloat(section, 'mac_idle')

        #Enter the NPU_Parameters
        section = 'NPU_parameters'

        self.npu_energy.sram_read = config.getfloat(section, 'sram_read')
        self.npu_energy.sram_write = config.getfloat(section, 'sram_write')
        self.npu_energy.dram_read = config.getfloat(section, 'dram_read')
        self.npu_energy.dram_write = config.getfloat(section, 'dram_write')
        self.npu_energy.mac_energy = self.get_mac_energy(npu_df)
        self.npu_energy.mac_idle = self.mac_energy.mac_idle

        #Enter the PIM_Parameters
        section = 'PIM_parameters'

        self.pim_energy.sram_read = config.getfloat(section, 'sram_read')
        self.pim_energy.sram_write = config.getfloat(section, 'sram_write')
        self.pim_energy.dram_read = config.getfloat(section, 'dram_read')
        self.pim_energy.dram_write = config.getfloat(section, 'dram_write')
        self.pim_energy.mac_energy = self.get_mac_energy(pim_df)
        self.pim_energy.mac_idle = self.mac_energy.mac_idle

    #Input: str / Return: float
    def get_mac_energy(self, dataflow) -> float:
        """If dataflow is OS, use mac_random, else use mac_reused."""
        if dataflow == "OS":
            energy = self.mac_energy.mac_random
        else:
            energy = self.mac_energy.mac_reused

        return energy

    #Input: str | str | str / Return: MACenergy | Energy | Energy
    def return_energy(self, path, npu_df, pim_df):
        """Return energy parameters."""
        self.get_energy(path, npu_df, pim_df)

        return self.npu_energy, self.pim_energy
