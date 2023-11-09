"Python 3.11.5"
import configparser as cp
import math

from .get_class import NPU_others
from .get_class import NPU_systolic
from .get_class import PIM_others
from .get_class import PIM_sysotlic
from .get_class import Other_params

class Getconfiguration:
    """Read hardware configuration and return."""
    def __init__(self):
        self.form_factor = ''
        self.npu_flag = False

        #NPU params
        self.npu_others = NPU_others(0,0,0,0,0,0,0)
        self.npu_systolic = NPU_systolic(128, 128, 0, 1536, 1536, 512)

        #PIM params
        self.pim_others = PIM_others(0,0,0,0,0,0,0,0)
        self.pim_systolic = PIM_sysotlic(128, 128, 1536, 1536, 512)

        #Other params
        self.other_params = Other_params(0,0)

    def read_config_file(self, path):
        """Read config file from file path"""
        config = cp.ConfigParser()
        config.read(path)

        section = 'Form_Factor'
        self.form_factor = config.get(section, 'form_factor')

        #Error check1: four form factors: ['Mobile', 'PC', 'Server', 'Supercomputer']
        if self.form_factor not in ['Mobile', 'PC', 'Server', 'Supercomputer']:
            raise Exception('Undefined form factor')

        if self.form_factor in ('Mobile', 'PC'):
            self.npu_flag = True
        else:
            self.npu_flag = False

        #NPU other parameters
        section = 'NPU_others'
        self.npu_others.pod_row = config.getint(section, 'pod_dimension_row')
        self.npu_others.pod_col = config.getint(section, 'pod_dimension_col')
        self.npu_others.num_pods = config.getint(section, 'number_of_pods')

        self.npu_others.clk_freq = config.getfloat(section, 'clock_frequency')
        self.npu_others.bandwidth = config.getfloat(section, 'bandwidth')
        self.npu_others.latency = config.getfloat(section, 'latency')
        self.npu_others.dataflow = config.get(section, 'dataflow')

        #NPU systolic array parameters
        section = 'NPU_systolic'
        if not self.npu_flag:
            self.npu_systolic.row = config.getint(section, 'row')
            self.npu_systolic.col = config.getint(section, 'col')
        else:
            throughput = config.getfloat(section, 'throughput')
            self.npu_systolic.row, self.npu_systolic.col, pod_row, pod_col = self.convert_throughput(\
                throughput, self.npu_others.pod_row, self.npu_others.pod_col, self.npu_others.clk_freq)
            self.npu_others.pod_row = pod_row
            self.npu_others.pod_col = pod_col

        self.npu_systolic.input_buffer = config.getfloat(section, 'input_buffer')
        self.npu_systolic.filter_buffer = config.getfloat(section, 'filter_buffer')
        self.npu_systolic.output_buffer = config.getfloat(section, 'output_buffer')

        #PIM other parameters
        section = 'PIM_others'
        self.pim_others.pod_row = config.getint(section, 'pod_dimension_row')
        self.pim_others.pod_col = config.getint(section, 'pod_dimension_col')

        self.pim_others.num_dimms = config.getint(section, 'number_of_dimms')
        self.pim_others.chips_per_dimm = config.getint(section, 'chips_per_dimm')

        self.pim_others.clk_freq = config.getfloat(section, 'clock_frequency')
        self.pim_others.bandwidth = config.getfloat(section, 'bandwidth')
        self.pim_others.latency = config.getfloat(section, 'latency')
        self.pim_others.dataflow = config.get(section, 'dataflow')

        #PIM systolic array paramters
        section = 'PIM_systolic'
        self.pim_systolic.row = config.getint(section, 'row')
        self.pim_systolic.col = config.getint(section, 'col')

        self.pim_systolic.input_buffer = config.getfloat(section, 'input_buffer')
        self.pim_systolic.filter_buffer = config.getfloat(section, 'filter_buffer')
        self.pim_systolic.output_buffer = config.getfloat(section, 'output_buffer')

        #Other parameters
        section = 'Other_parameters'
        self.other_params.batch = config.getint(section, 'batch')
        self.other_params.pim_flag = config.getboolean(section, 'pim_flag')


    #Input: float | int | int | float / Return: int | int | int | int
    def convert_throughput(self, throughput, pod_row, pod_col, clock_frequency):
        """Return converted throughput with throughput and h/w configuratinon."""

        num_pe = throughput * 1024 /(2 * clock_frequency)
        mul_two = int(round(math.log(num_pe) / math.log(2),0))

        if mul_two % 2 == 0:
            row = pow(2,int(mul_two/2))
            col = pow(2,int(mul_two/2))
        else:
            row = pow(2,int(mul_two/2))
            col = pow(2,int(mul_two/2)+1)
        #For row case
        if row % pod_row == 0:
            row_dim =  pod_row
            row = int(row / row_dim)
        else:
            print('NPU pod dimension row is set to 1: row % pod_row != 0')
            print('-----------------------------------------------------')
            row_dim = 1

        #For col case
        if col % pod_col == 0:
            col_dim = pod_col
            col = int(col / col_dim)
        else:
            print('NPU pod dimension column is set to 1: col % pod_col != 0')
            print('--------------------------------------------------------')
            col_dim = 1

        return row, col, row_dim, col_dim

    #Input: str / Return: str | list | list | Dnnsave
    def return_parameters(self, path):
        """Return params from configuration file."""
        self.read_config_file(path)

        return self.form_factor, self.npu_others, self.npu_systolic, self.pim_others, self.pim_systolic, self.other_params
