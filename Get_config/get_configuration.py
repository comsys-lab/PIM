"Python 3.11.5"
import configparser as cp
import math

from get_class import Systolic
from get_class import Npuothers
from get_class import Pimothers
from get_class import Dnnsave

from get_class import Others

class GetConfiguration:
    """Read hardware configuration and return."""
    def __init__(self):
        self.run_name = "run_name"
        self.form_factor = "Server"
        self.npu_flag = False

        #Return parameters
        self.npu_systolic = Systolic(128, 128, 1536, 1536, 512)
        self.npu_others = Others(0,0,0,0,0,0)

        self.pim_systolic = Systolic(128, 128, 1536, 1536, 512)
        self.pim_others = Others(0,0,0,0,0,0)

        self.dnn_save = Dnnsave()


        self.npu_param = [Systolic(128, 128, 1536, 1536, 512),
                           Npuothers(2, 2, 1, 1050, 12.8, 32, "WS")]
        self.pim_param = [Systolic(16, 16, 8, 8, 2), Pimothers(2 ,2 ,8, 32, 1024 ,512, "OS")]
        self.others = Dnnsave("", 0, True, "")

    def _read_config_file(self, path):
        "Read config file from file path"
        config = cp.ConfigParser()
        config.read(path)

        section = 'Form_Factor'
        self.form_factor = config.get(section, 'form_factor')

        if self.form_factor in ('Mobile', 'PC'):
            self.npu_flag = True
        else:
            self.npu_flag = False

        #NPU systolic array parameters
        section = 'NPU_systolic'
        if not self.npu_flag:
            self.npu_systolic.row = config.getint(section, 'row')
            self.npu_systolic.col = config.getint(section, 'col')
        else:
            npu_throughput = config.get(section, 'throughput')
            self.npu_systolic.row, self.npu_systolic.col = \
                self.convert_throughput(throughput, )
        self.npu_systolic.input_buf = config.getfloat(section, 'input_buffer')
        self.npu_systolic.filter_buf = config.getfloat(section, 'filter_buffer')
        self.npu_systolic.output_buf = config.getfloat(section, 'output_buffer')

        #NPU other parameters
        section = 'NPU_others'
        self.npu_others.pod_row = config.getint(section, 'pod_dimension_row')
        self.npu_others.pod_col = config.getint(section, 'pod_dimension_col')
        self.npu_others.num_pods = config.getint(section, ' number_of_pods')

        self.npu_others.clock_freq = config.getfloat(section, 'clock_frequency')
        self.npu_others.bandwidth = config.getfloat(section, 'bandwidth')
        self.npu_others.latency = config.getfloat(section, 'latency')
        self.npu_others.dataflow = config.get(section, 'dataflow')

        #PIM systolic array paramters
        section = 'PIM_systolic'
        self.pim_systolic.row = config.getint(section, 'row')
        self.pim_systolic.col = config.getint(section, 'col')

        self.npu_systolic.input_buf = config.getfloat(section, 'input_buffer')
        self.npu_systolic.filter_buf = config.getfloat(section, 'filter_buf')
        self.npu_systolic.output_buf = config.getfloat(section, 'output_buf')

        #PIM other parameters
        section = 'PIM_others'
        self.pim_others.row = config.getint(section, 'pod_dimension_row')
        self.pim_others.col = config.getint(section, 'pod_dimension_col')

        dimm = config.getint(section, 'number_of_dimms')
        chips = config.getint(section, 'chips_per_dimm')
        self.pim_others.num_pods = dimm * chips

        self.pim_others.clock_freq = config.getfloat(section, 'clock_frequency')
        self.pim_others.bandwidth = config.getfloat(section, 'bandwidth')
        self.pim_others.latency = config.getfloat(section, 'latency')
        self.pim_others.dataflow = config.get(section, 'dataflow')

    #Input: str
    def read_config_file(self, config_file):
        """From configuration file, read parameters."""
        config = cp.ConfigParser()
        config.read(config_file)

        #Enter Run name
        section = 'Run_name'
        self.run_name = config.get(section, 'Run_name')

        #In this section, we distribute form factor with two types: Mobile/PC, Server/Supercomputer.
        section = 'Form_Factor'
        self.form_factor = config.get(section, 'Form_Factor')


        if self.form_factor in ('Mobile', 'PC'):
            self.npu_flag = True
        else:
            self.npu_flag = False

        #In this section, we enter parameters for NPUs.
        section = 'NPU_Parameters'
        npu_sys = Systolic(0,0,0,0,0)
        npu_otherparams = Npuothers(0,0,0,0,0,0,"")

        npu_sys.input_buffer = config.getint(section, 'input_buffer')
        npu_sys.filter_buffer = config.getint(section, 'filter_buffer')
        npu_sys.output_buffer = config.getint(section, 'output_buffer')

        npu_otherparams.pod_dimension_row = config.getint(section, 'pod_dimension_row')
        npu_otherparams.pod_dimension_col = config.getint(section, 'pod_dimension_col')
        npu_otherparams.number_of_pods = config.getint(section, 'number_of_pods')

        npu_otherparams.clock_frequency = config.getfloat(section, 'clock_frequency')
        npu_otherparams.bandwidth_per_dimm = config.getfloat(section, 'bandwidth_per_dimm')
        npu_otherparams.number_of_dimms = config.getint(section, 'number_of_dimms')
        npu_otherparams.dataflow = config.get(section, 'dataflow')

        if self.npu_flag is True:
            throughput = config.getfloat(section, 'throughput')
            npu_sys.systolic_row, npu_sys.systolic_col, npu_otherparams.pod_dimension_row,\
            npu_otherparams.pod_dimension_col = self.convert_throughput(throughput,
            npu_otherparams.pod_dimension_row, npu_otherparams.pod_dimension_col,
            npu_otherparams.clock_frequency)

        else:
            npu_sys.systolic_row = config.getint(section, 'systolic_row')
            npu_sys.systolic_col = config.getint(section, 'systolic_col')
        self.npu_param[0] = npu_sys
        self.npu_param[1] = npu_otherparams

        #In this section, enter the parameters for PIM units.
        section = 'PIM_Parameters'
        pim_sys = Systolic(0,0,0,0,0)
        pim_otherparams = Pimothers(0,0,0,0,0,0,"")

        pim_sys.systolic_row = config.getint(section, 'systolic_row')
        pim_sys.systolic_col = config.getint(section, 'systolic_col')
        pim_sys.input_buffer = config.getfloat(section, 'input_buffer')
        pim_sys.filter_buffer = config.getfloat(section, 'filter_buffer')
        pim_sys.output_buffer = config.getfloat(section, 'output_buffer')

        pim_otherparams.pod_dimension_row = config.getint(section, 'pod_dimension_row')
        pim_otherparams.pod_dimension_col = config.getint(section, 'pod_dimension_col')
        pim_otherparams.chips_per_dimm = config.getint(section, 'chips_per_dimm')
        pim_otherparams.number_of_dimms = config.getint(section, 'number_of_dimms')

        pim_otherparams.clock_frequency = config.getfloat(section, 'clock_frequency')
        pim_otherparams.bandwidth_per_dimm = config.getfloat(section, 'bandwidth_per_dimm')
        pim_otherparams.dataflow = config.get(section, 'dataflow')
        self.pim_param[0] = pim_sys
        self.pim_param[1] = pim_otherparams

        #In this section, enter the parameters for DNN Models.
        section = 'DNN_Parameters'
        self.others.topology_path = config.get(section, 'topology_path')
        self.others.batch = config.getint(section, 'batch')

        #In this section, eneter the parameters for saving results.
        section = 'Save_Parameters'
        self.others.pim_flag = config.getboolean(section, 'pim_flag')
        self.others.storing_path = config.get(section, 'storing_path')

    #Input: float | int | int | float / Return: int | int | int | int
    def convert_throughput(self, throughput, pod_row, pod_col, clock_frequency):
        """
        Throughput = 2 * # of pod * clock frequency
        #of pod = Throughput / (2 * clock frequency)
        """

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

        return self.run_name, self.npu_param, self.pim_param, self.others
