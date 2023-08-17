"Python 3.10.8"
from dataclasses import dataclass
import configparser as cp
import math

@dataclass
class Systolic:
    """Define systolic array's dimension."""
    systolic_row: int
    systolic_col: int

    input_buffer: float
    filter_buffer: float
    output_buffer: float

@dataclass
class Npuothers:
    """Dataclass for npu's other parameters."""
    pod_dimension_row: int
    pod_dimension_col: int
    number_of_pods: int

    clock_frequency: float
    bandwidth_per_dimm: float
    number_of_dimms: int
    dataflow: str

@dataclass
class Pimothers:
    """Dataclass for pim's other parameters."""
    pod_dimension_row: int
    pod_dimension_col: int
    chips_per_dimm: int
    number_of_dimms: int

    clock_frequency: int
    bandwidth_per_dimm: float
    dataflow: str

@dataclass
class Dnnsave:
    """Dataclass for saving dnn and save parameters."""
    topology_path: str
    batch: int

    pim_flag: bool
    storing_path: str

class GetConfiguration:
    """Read hardware configuration and return."""
    def __init__(self):
        self.run_name = "run_name"
        self.form_factor = "Server"
        self.npu_flag = False

        #Return parameters
        self.npu_param = [Systolic(128, 128, 1536, 1536, 512),
                           Npuothers(2, 2, 1, 1050, 12.8, 32, "WS")]
        self.pim_param = [Systolic(16, 16, 8, 8, 2), Pimothers(2 ,2 ,8, 32, 1024 ,512, "OS")]
        self.others = Dnnsave("", 0, True, "")

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

    def return_parameters(self, path):
        """Return params from configuration file."""
        self.read_config_file(path)

        return self.run_name, self.npu_param, self.pim_param, self.others