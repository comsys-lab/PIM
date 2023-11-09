"Python 3.11.5"

from Get_configuration.get_topology import GetTopology
from Get_configuration.get_configuration import Getconfiguration
from Get_configuration.get_energy import GetEnergy

from Scaleout.Scaleup.base_class import Scaleout
from Scaleout.Scaleup.base_class import Scaleup
from Scaleout.Scaleup.base_class import Operand
from Scaleout.Scaleup.base_class import Systolic
from Scaleout.Scaleup.base_class import Others

class Simulation_settings:
    """Simulation setting code."""
    def __init__(self):
        self.get_topology = GetTopology()
        self.get_configuration = Getconfiguration()
        self.get_energy = GetEnergy()

    def simulation_settings(self, topo_path, config_path, energy_path):
        """Get configurations from hardware, topology, energy configuration files."""
        _, _, topo, mac = self.get_topology.get_topology(topo_path)
        form_factor, npu_others, npu_systolic, pim_others, pim_systolic, other_params = \
        self.get_configuration.return_parameters(config_path)
        npu_energy, pim_energy = self.get_energy.return_energy(energy_path, npu_others.dataflow, pim_others.dataflow)

        npu_scaleout = self.npu_params_set(npu_systolic, npu_others)
        pim_scaleout = self.pim_params_set(pim_systolic, pim_others)

        return topo, mac, form_factor, npu_scaleout, pim_scaleout, npu_energy, pim_energy, other_params, npu_others, pim_others

    def npu_params_set(self, NPU_systolic, NPU_others):
        """Function for NPU parameters setting."""
        npu_scaleout = Scaleout(Scaleup(None,None),Operand(None,None),None,None)

        #Get NPU systolic array parameters
        npu_systolic = Systolic(None,None,None,None,None)

        npu_systolic.row = NPU_systolic.row
        npu_systolic.col = NPU_systolic.col
        npu_systolic.input_buffer = NPU_systolic.input_buffer
        npu_systolic.filter_buffer = NPU_systolic.filter_buffer
        npu_systolic.output_buffer = NPU_systolic.output_buffer

        #Get NPU others parameters
        npu_others = Others(None,None,None,None)

        npu_others.latency = NPU_others.latency
        npu_others.bandwidth = NPU_others.bandwidth
        npu_others.dataflow = NPU_others.dataflow
        npu_others.clk_freq = NPU_others.clk_freq

        total_chips = NPU_others.pod_row * NPU_others.pod_col
        npu_others.bandwidth = self.convert_bandwidth(npu_others.bandwidth, total_chips, npu_others.clk_freq)

        npu_scaleout.scaleup.systolic = npu_systolic
        npu_scaleout.scaleup.others = npu_others
        npu_scaleout.row_dim = NPU_others.pod_row
        npu_scaleout.col_dim = NPU_others.pod_col

        return npu_scaleout

    def pim_params_set(self, PIM_systolic, PIM_others):
        """Function for PIM parameters setting."""
        pim_scaleout = Scaleout(Scaleup(None,None),Operand(None,None),None,None)

        #Get PIM systolic array parameters
        pim_systolic = Systolic(None,None,None,None,None)

        pim_systolic.row = PIM_systolic.row
        pim_systolic.col = PIM_systolic.col
        pim_systolic.input_buffer = PIM_systolic.input_buffer
        pim_systolic.filter_buffer = PIM_systolic.filter_buffer
        pim_systolic.output_buffer = PIM_systolic.output_buffer

        #Get PIM others parameters
        pim_others = Others(None,None,None,None)

        pim_others.latency = PIM_others.latency
        pim_others.bandwidth = PIM_others.bandwidth
        pim_others.dataflow = PIM_others.dataflow
        pim_others.clk_freq = PIM_others.clk_freq

        total_chips = PIM_others.chips_per_dimm * PIM_others.pod_row * PIM_others.pod_col
        pim_others.bandwidth = self.convert_bandwidth(pim_others.bandwidth, total_chips, pim_others.clk_freq)

        pim_scaleout.scaleup.systolic = pim_systolic
        pim_scaleout.scaleup.others = pim_others
        pim_scaleout.row_dim = PIM_others.pod_row
        pim_scaleout.col_dim = PIM_others.pod_col

        return pim_scaleout

    def convert_bandwidth(self, bandwidth, total_chips, clk_freq):
        """Convert bandwidth to cycle."""
        #BW = GB/s, clk_freq = MHz
        bw_per_cycle = round(bandwidth * 1024 / (2 * total_chips * clk_freq),2)

        return bw_per_cycle
