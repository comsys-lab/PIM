"Python 3.11.5"
import multiprocessing
import sys
sys.path.append('/Users/seongjun/Desktop/PIM/')

from Get_config.get_topology import GetTopology
from Get_config.get_configuration import Getconfiguration
from Get_config.get_energy import GetEnergy

from scaleout.scaleout_class import Scaleout
from scaleout.Scaleup.scaleup_class import Systolic

class Simulation:
    """Simulation code."""
    def __init__(self) -> None:
        self.get_topology = GetTopology()
        self.get_configuration = Getconfiguration()
        self.get_energy = GetEnergy()

        self.npu_scaleout = Scaleout(0,0,0,0)
        self.pim_scaleout = Scaleout(0,0,0,0)

        self.topo = []
        self.mnk = []
        self.new_topo = []
        self.mac = 0

        self.npu_others = []
        self.npu_systolic = []
        self.pim_others = []
        self.pim_systolic = []
        self.other_params = []

        self.npu_energy = []
        self.pim_energy = []


    def simulation_settings(self, topo_path, config_path, energy_path):
        """."""
        self.topo, self.mnk, self.new_topo, self.mac = self.get_topology.get_topology(topo_path)
        self.npu_others, self.npu_systolic, self.pim_others, self.pim_systolic, self.other_params = \
        self.get_configuration.return_parameters(config_path)
        self.npu_energy, self.pim_energy = self.get_energy.return_energy(energy_path, self.npu_others.dataflow, self.pim_others.dataflow)

    def simulation(self, topo_path, config_path, energy_path):
        """Simulation code."""
        self.simulation_settings(topo_path, config_path, energy_path)

        if self.other_params[2]:
            self.with_pim()
        else:
            self.only_npu()

    def npu_param_setting(self):
        """."""
        npu_row = self.npu_systolic[0]
        npu_col = self.npu_systolic[1]
        npu_input_buf = self.npu_systolic[2]
        npu_filter_buf = self.npu_systolic[3]
        npu_output_buf = self.npu_systolic[4]
        self.npu_scaleout.scaleup = Systolic(npu_row, npu_col, npu_input_buf, npu_filter_buf, npu_output_buf)

        row_dim = self.npu_others[0]
        col_dim = self.npu_others[1]
        self.num_npu_pods = self.npu_others[2]

        npu_clock_freq = self.npu_others[3]
        npu_bandwidth = self.npu_others[4]
        npu_latency = self.npu_others[5]
        self.npu_dataflow = self.npu_others[6]

    def convert_bandwidth(self):
        pass

    def pim_param_setting(self):
        pim_row = self.pim_systolic[0]
        pim_col = self.pim_systolic[1]
        pim_input_buf = self.pim_systolic[2]
        pim_filter_buf = self.pim_systolic[3]
        pim_output_buf = self.pim_systolic[4]
        self.pim_scaleout.scaleup = Systolic(pim_row, pim_col, pim_input_buf, pim_filter_buf, pim_output_buf)

    def only_npu(self):
        """Only NPU"""
        if self.other_params[1] == 1:
            self.npu_batch_one()
        else:
            self.npu_batch_over_one()
        for one_layer in self.topo:
            self.one_layer(one_layer)

    def with_pim(self):
        """With PIM"""
        if self.other_params[1] == 1:
            self.pim_batch_one()
        else:
            self.pim_batch_over_one()


import os
path = os.getcwd()
topo_path = path + '/_Topology/ex.csv'
config_path = path + '/_Hardware/configuration2.cfg'
energy_path = path + '/_Energy/Energy_Config1.cfg'

a = Simulation()
a.simulation(topo_path, config_path, energy_path)
print(a.npu_energy)