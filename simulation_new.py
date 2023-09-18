"Python 3.11.5"

from Get_config.get_topology import GetTopology
from Get_config.get_configuration import Getconfiguration
from Get_config.get_energy import GetEnergy



class simulation_new:
    """Simulation code."""
    def __init__(self) -> None:
        self.get_topology = GetTopology()
        self.get_configuration = Getconfiguration()
        self.get_energy = GetEnergy()

    def simulation_settings(self, topo_path, config_path, energy_path):
        self.topo, self.mnk, self.new_topo, self.mac = self.get_topology.get_topology(topo_path)
        self.npu_others, self.npu_systolic, self.pim_others, self.pim_systolic, self.other_params = \
        self.get_configuration.return_parameters(config_path)
        self.npu_energy, self.pim_energy = self.get_energy.return_energy(energy_path, self.npu_others.dataflow, self.pim_others.dataflow)

    def simulation(self, topo_path, config_path, energy_path):
        self.simulation_settings(topo_path, config_path, energy_path)



"""
a = simulation_new()
a.simulation('/Users/seongjun/Desktop/PIM/_Topology/ex.csv','/Users/seongjun/Desktop/PIM/_Hardware/configuration2.cfg','/Users/seongjun/Desktop/PIM/_Energy/Energy_Config1.cfg')
"""