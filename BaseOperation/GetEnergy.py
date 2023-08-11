from dataclasses import dataclass
import configparser as cp

@dataclass
class MAC_energy:
    """MAC parameters"""
    MAC_random: float
    MAC_reused: float
    MAC_gated: float
    MAC_idle: float

@dataclass
class NPU_energy:
    """energy parameters"""
    SRAM_read: float
    SRAM_write: float
    DRAM_read: float
    DRAM_write: float
    MAC_energy: float
    MAC_idle: float

@dataclass
class PIM_energy:
    """ energy parameters"""
    SRAM_read: float
    SRAM_write: float
    DRAM_read: float
    DRAM_write: float
    MAC_energy: float
    MAC_idle: float

class GetEnergy:
    """ Get energy parameters from configuration file (.cfg) """
    def __init__(self):
        self.mac_energy = MAC_energy(0,0,0,0)
        self.npu_energy = NPU_energy(0,0,0,0,0,0)
        self.pim_energy = PIM_energy(0,0,0,0,0,0)

    def GetEnergy(self, path, npu_dataflow, pim_dataflow):
        """Get energy parameters from configuration file path"""
        config = cp.ConfigParser()
        config.read(path)

        #Enter the MAC_Parameters
        section = 'MAC_Parameters'

        self.mac_energy.MAC_random = config.getfloat(section, 'MAC_random')
        self.mac_energy.MAC_reused = config.getfloat(section, 'MAC_reused')
        self.mac_energy.MAC_gated = config.getfloat(section, 'MAC_gated')
        self.mac_energy.MAC_idle = config.getfloat(section, 'MAC_idle')

        #Enter the NPU_Parameters
        section = 'NPU_Parameters'

        self.npu_energy.SRAM_read = config.getfloat(section, 'SRAM_read')
        self.npu_energy.SRAM_write = config.getfloat(section, 'SRAM_write')
        self.npu_energy.DRAM_read = config.getfloat(section, 'DRAM_read')
        self.npu_energy.DRAM_write = config.getfloat(section, 'DRAM_write')
        self.npu_energy.MAC_energy = self._get_mac_energy(npu_dataflow)
        self.npu_energy.MAC_idle = self.mac_energy.MAC_idle

        #Enter the PIM_Parameters
        section = 'PIM_Parameters'

        self.pim_energy.SRAM_read = config.getfloat(section, 'SRAM_read')
        self.pim_energy.SRAM_write = config.getfloat(section, 'SRAM_write')
        self.pim_energy.DRAM_read = config.getfloat(section, 'DRAM_read')
        self.pim_energy.DRAM_write = config.getfloat(section, 'DRAM_write')
        self.pim_energy.MAC_energy = self._get_mac_energy(pim_dataflow)
        self.pim_energy.MAC_idle = self.mac_energy.MAC_idle

    def _get_mac_energy(self, dataflow):
        """ If dataflow is OS, use mac_random, else use mac_reused. """
        if dataflow is "OS":
            return self.mac_energy.MAC_random
        else:
            return self.mac_energy.MAC_reused

    def return_energy_parameters(self):
        """ Return energy parameters. """
        return self.mac_energy, self.npu_energy, self.pim_energy