"Python 3.11.5"
import sys
import os
path = os.getcwd()
sys.path.append(path)

from Get_configuration.get_topology import GetTopology
from Get_configuration.get_configuration import Getconfiguration
from Get_configuration.get_energy import GetEnergy

from Make_Operand.make_operand import MakeOperand

from Scaleout.scaleout import ScaleOut


from Scaleout.Scaleup.base_class import Scaleout
from Scaleout.Scaleup.base_class import Scaleup
from Scaleout.Scaleup.base_class import Operand
from Scaleout.Scaleup.base_class import Operand
from Scaleout.Scaleup.base_class import Systolic
from Scaleout.Scaleup.base_class import Others

class Simulation:
    """Simulation code."""
    def __init__(self):
        self.get_topology = GetTopology()
        self.get_configuration = Getconfiguration()
        self.get_energy = GetEnergy()

        self.make_operand = MakeOperand()

        self.scaleout = ScaleOut()

        self.npu_scaleout = Scaleout(Scaleup(None,None),Operand(None,None),None,None)
        self.pim_scaleout = Scaleout(Scaleup(None,None),Operand(None,None),None,None)

    def simulation_settings(self, topo_path, config_path, energy_path, storage_path):
        """Get configurations from hardware, topology, energy configuration files."""
        self.topo, self.mnk, self.new_topo, self.mac = self.get_topology.get_topology(topo_path)
        self.form_factor, self.npu_others, self.npu_systolic, self.pim_others, self.pim_systolic, self.other_params = \
        self.get_configuration.return_parameters(config_path)
        self.npu_energy, self.pim_energy = self.get_energy.return_energy(energy_path, self.npu_others.dataflow, self.pim_others.dataflow)
        self.storage_path = storage_path
        self.npu_scaleout = self.npu_params_set()
        self.pim_scaleout = self.pim_params_set()

    def npu_params_set(self):
        """Function for NPU parameters setting."""
        npu_scaleout = Scaleout(Scaleup(None,None),Operand(None,None),None,None)

        #Get NPU systolic array parameters
        npu_systolic = Systolic(None,None,None,None,None)

        npu_systolic.row = self.npu_systolic.row
        npu_systolic.col = self.npu_systolic.col
        npu_systolic.input_buffer = self.npu_systolic.input_buffer
        npu_systolic.filter_buffer = self.npu_systolic.filter_buffer
        npu_systolic.output_buffer = self.npu_systolic.output_buffer

        #Get NPU others parameters
        npu_others = Others(None,None,None,None)

        npu_others.latency = self.npu_others.latency
        npu_others.bandwidth = self.npu_others.bandwidth
        npu_others.dataflow = self.npu_others.dataflow
        npu_others.clk_freq = self.npu_others.clk_freq

        total_chips = self.npu_others.pod_row * self.npu_others.pod_col
        npu_others.bandwidth = self.convert_bandwidth(npu_others.bandwidth, total_chips, npu_others.clk_freq)

        npu_scaleout.scaleup.systolic = npu_systolic
        npu_scaleout.scaleup.others = npu_others
        npu_scaleout.row_dim = self.npu_others.pod_row
        npu_scaleout.col_dim = self.npu_others.pod_col

        return npu_scaleout

    def pim_params_set(self):
        """Function for PIM parameters setting."""
        pim_scaleout = Scaleout(Scaleup(None,None),Operand(None,None),None,None)

        #Get PIM systolic array parameters
        pim_systolic = Systolic(None,None,None,None,None)

        pim_systolic.row = self.pim_systolic.row
        pim_systolic.col = self.pim_systolic.col
        pim_systolic.input_buffer = self.pim_systolic.input_buffer
        pim_systolic.filter_buffer = self.pim_systolic.filter_buffer
        pim_systolic.output_buffer = self.pim_systolic.output_buffer

        #Get PIM others parameters
        pim_others = Others(None,None,None,None)

        pim_others.latency = self.pim_others.latency
        pim_others.bandwidth = self.pim_others.bandwidth
        pim_others.dataflow = self.pim_others.dataflow
        pim_others.clk_freq = self.pim_others.clk_freq

        total_chips = self.pim_others.chips_per_dimm * self.pim_others.pod_row * self.pim_others.pod_col
        pim_others.bandwidth = self.convert_bandwidth(pim_others.bandwidth, total_chips, pim_others.clk_freq)

        pim_scaleout.scaleup.systolic = pim_systolic
        pim_scaleout.scaleup.others = pim_others
        pim_scaleout.row_dim = self.pim_others.pod_row
        pim_scaleout.col_dim = self.pim_others.pod_col

        return pim_scaleout

    def convert_bandwidth(self, bandwidth, total_chips, clk_freq):
        """Convert bandwidth to cycle."""
        #BW = GB/s, clk_freq = MHz
        bw_per_cycle = round(bandwidth * 1024 / (2 * total_chips * clk_freq),2)

        return bw_per_cycle

    def mobile(self):
        if self.other_params.pim_flag == True: #With PIM
            pass
        else: #Only NPU
            pass

    def other_form_factor(self):
        if self.other_params.pim_flag == True: #With PIM
            pass
        else: #Only NPU
            pass




    def mobile_with_pim(self):
        pass

    #Assume entire layer simulation
    def pim_simulation(self):
        sram_store = []
        dram_sore = []
        runtime_store = []

    #Assume entire layer simulation
    def npu_simulation(self):
        """NPU simulation code."""
        results = []
        print('NPU simulation\n')
        length = len(self.new_topo)
        for idx in range(length):
            topo = self.new_topo[idx][1]
            input_operand, filter_operand = self.make_operand.return_operand_matrix(topo, self.npu_scaleout.scaleup.others.dataflow)
            stride = topo[-1]
            layer_info = [idx, length]
            self.npu_scaleout.operand.input_operand = input_operand
            self.npu_scaleout.operand.filter_operand = filter_operand
            #Scaleout function
            sram_info, dram_info, runtime, ene_eff = self.scaleout.scaleout(self.npu_scaleout, stride, layer_info)

    def store_information(self):
        """Store information into csv file."""
        path_name = ''
        file = open(path_name, 'w')
        #Write Hardware configuration and topology name, and energy configuration name.
        file.write('Hardware configuration: ' + self.config_path + '\n')
        file.write('Topology: ' + self.topo_path + '\n')
        file.write('Energy configuration: ' + self.energy_path + '\n')


    def simulation(self, topo_path, config_path, energy_path, storage_path):
        """Simulation code."""
        self.simulation_settings(topo_path, config_path, energy_path, storage_path)

        self.npu_simulation()

    def etc(self):
        if self.form_factor == 'Mobile' and self.other_params.pim_flag == True:
            self.mobile_with_pim()
        else:
            if self.pim_flag == True:
                self.npu_simulation()
                self.pim_simulation()
            else:
                self.npu_simulation()

        #Simulation function need to be generated
        # if self.form_factor == 'Mobile':
        #     self.mobile()

        # else:
        #     self.other_form_factor()



import os
path = os.getcwd()
topo_path = path + '/_Topology/VIT/ViT_base_196.csv'
config_path = path + '/_Hardware/configuration2.cfg'
energy_path = path + '/_Energy/Energy_Config1.cfg'
storage_path = path
a = Simulation()
a.simulation(topo_path, config_path, energy_path, storage_path)
