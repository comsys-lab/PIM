"Python 3.11.5"
import sys
import os
path = os.getcwd()
sys.path.append(path)

import numpy as np

from simulation_setting import Simulation_settings

from Get_configuration.get_topology import GetTopology
from Get_configuration.get_configuration import Getconfiguration
from Get_configuration.get_energy import GetEnergy

from Make_Operand.make_operand import MakeOperand

from Scaleout.scaleout import ScaleOut

from Scaleout.Scaleup.base_class import Scaleout
from Scaleout.Scaleup.base_class import Scaleup
from Scaleout.Scaleup.base_class import Operand

from Scaleout.Scaleup.scaleup_runtime import Scaleupruntime

from mobile_distribution import MobileDistribution()

class Simulation:
    """Simulation code."""
    def __init__(self):
        self.simulation_settings = Simulation_settings()

        self.get_topology = GetTopology()
        self.get_configuration = Getconfiguration()
        self.get_energy = GetEnergy()

        self.make_operand = MakeOperand()

        self.scaleout = ScaleOut()

        self.scaleup_runtime = Scaleupruntime()

        self.mobile_distribution = MobileDistribution()

        self.npu_scaleout = Scaleout(Scaleup(None,None),Operand(None,None),None,None)
        self.pim_scaleout = Scaleout(Scaleup(None,None),Operand(None,None),None,None)

    #Assume entire layer simulation
    def pim_simulation(self):
        """NPU simulation code."""

        result_list = []

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
            results = self.scaleout.scaleout(self.pim_scaleout, stride, layer_info)
            result_list.append(results)
        print('PIM Simulation Complete\n')

        return result_list

    #Assume entire layer simulation
    def npu_simulation(self):
        """NPU simulation code."""

        result_list = []

        print('NPU Simulation Start\n')
        length = len(self.topo)
        for idx in range(length):
            topo = self.topo[idx][1]
            input_operand, filter_operand = self.make_operand.return_operand_matrix(topo, self.npu_scaleout.scaleup.others.dataflow)
            stride = topo[-1]
            layer_info = [idx, length]
            self.npu_scaleout.operand.input_operand = input_operand
            self.npu_scaleout.operand.filter_operand = filter_operand

            #Scaleout function
            results = self.scaleout.scaleout(self.npu_scaleout, stride, layer_info)
            result_list.append(results)
        print('NPU Simulation Complete\n')

        return result_list

    def check_filter(self):
        """Check filter size."""
        filter_size = 0
        for topo in self.topo:
            filter_size += np.ceil(topo[1][4] * topo[1][5] / self.npu_scaleout.col_dim)
        """
        filter_size = self.check_filter()
        if self.npu_scaleout.scaleup.systolic.input_buffer >= filter_size:
            filter_dram = filter_size
        """
        return filter_size

    def mobile_with_pim(self, default_path):
        """Case 1: Mobile with PIM."""
        row = self.pim_scaleout.row_dim * self.pim_scaleout.col_dim
        col = self.pim_others.chips_per_dimm

        self.pim_scaleout.row_dim = row
        self.pim_scaleout.col_dim = col

        length = len(self.topo)
        for idx in range(length):
            topo = self.topo[idx][1]
            npu_input, npu_filter = self.make_operand.return_operand_matrix(topo, self.npu_scaleout.scaleup.others.dataflow)
            pim_input, pim_filter = self.make_operand.return_operand_matrix(topo, self.pim_scaleout.scaleup.others.dataflow)
            stride = topo[-1]
            layer_info = [idx, length]

            pim_return, npu_return, didx = self.mobile_distribution(npu_input, npu_filter, pim_input, pim_filter, stride)
            print(pim_return, npu_return, didx)
            # self.npu_scaleout.operand.input_operand = input_operand
            # self.npu_scaleout.operand.filter_operand = filter_operand

            # #Scaleout function
            # results = self.scaleout.scaleout(self.npu_scaleout, stride, layer_info)
            # result_list.append(results)
        return 1,1,1
        # return something

    def other_simulation(self, default_path):
        npu_result_list = self.npu_simulation()
        pim_result_list = self.pim_simulation()

        npu_runtime = 0
        pim_runtime = 0
        length = len(npu_result_list)
        for idx in range(length):
            npu_runtime += npu_result_list[idx].runtime * self.topo[idx][0]
            pim_runtime += pim_result_list[idx].runtime * self.topo[idx][0]

        npu_batch, pim_batch = self.batch_distribution(npu_runtime, pim_runtime)

    def results_write(self):
        pass

    def batch_distribution(self, npu_runtime, pim_runtime):
        """Return batch distribution."""
        npu_total = self.npu_others.num_pods
        pim_total = self.pim_others.num_dimms * self.pim_others.chips_per_dimm

        runtime = 100000000000000
        batch_size = self.other_params.batch
        for batch in range(1,batch_size):
            npu_runtime_temp = np.ceil((batch_size - batch) /npu_total)* npu_runtime
            pim_runtime_temp = np.ceil(batch/pim_total)* pim_runtime
            runtime_temp = max(npu_runtime_temp ,pim_runtime_temp)
            if runtime_temp < runtime:
                runtime = runtime_temp
                batch_var = batch

        npu_batch = batch_size - batch_var
        pim_batch = batch_var

        return npu_batch, pim_batch

    def store_file_name(self, topo_path, config_path, energy_path, storage_path):
        """Store information into csv file."""
        #Storing file name must be store in order of hardware configuration.
        topo_name = topo_path.split('/')[-1].split('.')[0]
        energy_name = energy_path.split('/')[-1].split('.')[0]
        energy_path = energy_name.split('_')[-1]
        configuration_name  = config_path.split('/')[-2] + '_' + config_path.split('/')[-1].split('.')[0]

        if storage_path[-1] != '/':
            storage_path += '/'

        default_path = storage_path + topo_name + '/' + energy_path + '/' + energy_name + '_' + configuration_name + '.csv'
        dir_path = storage_path + topo_name + '/' + energy_path + '/' + energy_name + '/' + str(self.pim_others.num_dimms)

        if not os.path.exists(dir_path):
            os.makedirs(dir_path)

        return default_path

    def simulation(self, topo_path, config_path, energy_path, storage_path):
        """Simulation code."""
        self.topo, self.mac, self.form_factor, self.npu_scaleout, self.pim_scaleout, self.npu_energy, self.pim_energy, self.other_params,\
            self.npu_others, self.pim_others = self.simulation_settings.simulation_settings(topo_path, config_path, energy_path)
        self.storage_path = storage_path
        default_path = self.store_file_name(topo_path, config_path, energy_path, storage_path)

        if self.form_factor == 'Mobile':
            self.mobile_with_pim(default_path)
        else:
            self.other_simulation(default_path)

import os
path = os.getcwd()
topo_path = path + '/_Topology/BERT_Large/BERT_large_512.csv'
config_path = path + '/_Hardware/Mobile.cfg'
energy_path = path + '/_Energy/DDR4/DDR4_8KB.cfg'
storage_path = path
a = Simulation()
a.simulation(topo_path, config_path, energy_path, storage_path)
