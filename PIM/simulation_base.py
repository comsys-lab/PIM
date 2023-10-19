"Python 3.11.5"
import sys
import os
path = os.getcwd()
sys.path.append(path)

from simulation_setting import Simulation_settings

from Get_configuration.get_topology import GetTopology
from Get_configuration.get_configuration import Getconfiguration
from Get_configuration.get_energy import GetEnergy

from Make_Operand.make_operand import MakeOperand

from Scaleout.scaleout import ScaleOut

from Scaleout.Scaleup.base_class import Scaleout
from Scaleout.Scaleup.base_class import Scaleup
from Scaleout.Scaleup.base_class import Operand

class Simulation:
    """Simulation code."""
    def __init__(self):
        self.simulation_settings = Simulation_settings()

        self.get_topology = GetTopology()
        self.get_configuration = Getconfiguration()
        self.get_energy = GetEnergy()

        self.make_operand = MakeOperand()

        self.scaleout = ScaleOut()

        self.npu_scaleout = Scaleout(Scaleup(None,None),Operand(None,None),None,None)
        self.pim_scaleout = Scaleout(Scaleup(None,None),Operand(None,None),None,None)

    #Assume entire layer simulation
    def pim_simulation(self):
        sram_store = []
        dram_sore = []
        runtime_store = []

        print('PIM Simulation Starts\n')
        length = len(self.topo)
        for idx in range(length):
            topo = self.topo[idx][1]
            input_operand, filter_operand = self.make_operand.return_operand_matrix(topo, self.pim_scaleout.scaleup.others.dataflow)
            stride = topo[-1]
            layer_info = [idx, length]
            self.pim_scaleout.operand.input_operand = input_operand
            self.pim_scaleout.operand.filter_operand = filter_operand
            #Scaleout function
            sram_info, dram_info, runtime, ene_eff = self.scaleout.scaleout(self.pim_scaleout, stride, layer_info)

    #Assume entire layer simulation
    def npu_simulation(self):
        """NPU simulation code."""
        sram_result = []
        dram_result = []
        runtime_result = []

        print('NPU Simulation Starts\n')
        length = len(self.topo)
        for idx in range(length):
            topo = self.topo[idx][1]
            input_operand, filter_operand = self.make_operand.return_operand_matrix(topo, self.npu_scaleout.scaleup.others.dataflow)
            stride = topo[-1]
            layer_info = [idx, length]
            self.npu_scaleout.operand.input_operand = input_operand
            self.npu_scaleout.operand.filter_operand = filter_operand
            #Scaleout function
            sram_info, dram_info, runtime, ene_eff = self.scaleout.scaleout(self.npu_scaleout, stride, layer_info)
            sram_result.append(sram_info)
            dram_result.append(dram_info)
            runtime_result.append(runtime)

        return sram_result, dram_result, runtime_result

    def store_file_name(self, topo_path, config_path, storage_path):
        """Store information into csv file."""
        #Storing file name must be store in order of hardware configuration.
        configuration_name  = config_path.split('/')[-2] + '_' + config_path.split('/')[-1].split('.')[0]
        topo_name = topo_path.split('/')[-1].split('.')[0]
        file_name = '_' + configuration_name + '_' + topo_name +'.csv'
        default_path = storage_path + file_name

        return default_path

    def simulation(self, topo_path, config_path, energy_path, storage_path):
        """Simulation code."""
        self.topo, self.mac, self.form_factor, self.npu_scaleout, self.pim_scaleout, self.npu_energy, self.pim_energy, self.other_params=\
            self.simulation_settings.simulation_settings(topo_path, config_path, energy_path)
        self.storage_path = storage_path
        deafult_path = self.store_file_name(topo_path, config_path, storage_path)

        if self.form_factor == 'Mobile':
            if self.other_params.pim_flag == True:
                runtime, energy_consumption, performance_per_watt = self.mobile_with_pim()
            else:
                runtime, energy_consumption, performance_per_watt = self.only_npu()
        else:
            if self.other_parmas.pim_flag == True:
                runtime, energy_consumption, performance_per_watt = self.with_pim()
            else:
                runtime, energy_consumption, performance_per_watt = self.only_npu()

    #Four case exists, mobile/ not mobile, pim/with pim

    def mobile_with_pim(self):
        """Case 1: Mobile with PIM."""
        pass

    def only_npu(self):
        """Case 2: Only NPU."""
        pass

    def with_pim(self):
        """Case 3: Not mobile with PIM."""
        pass

import os
path = os.getcwd()
topo_path = path + '/_Topology/VIT/ViT_base_196.csv'
config_path = path + '/_Hardware/DDR4/configuration2.cfg'
energy_path = path + '/_Energy/Energy_Config1.cfg'
storage_path = path
a = Simulation()
a.simulation(topo_path, config_path, energy_path, storage_path)
