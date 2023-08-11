"Python 3.10.8"
from dataclasses import dataclass
import configparser as cp
import math

@dataclass
class Systolic:
    """ Define systolic array's dimension"""
    systolic_row: int
    systolic_col: int

    input_buffer: float
    filter_buffer: float
    output_buffer: float

@dataclass
class Others:
    """."""
    pod_dimension_row: int
    pod_dimension_col: int
    number_of_chip: int

    clock_frequency: float
    bandwidth_per_dimm: float
    dataflow: str

class GetConfiguration:
    """."""
    def __init__(self):
        self.run_name = "run_name"
        self.form_factor = "Server"
        self.npu_flag = False

        #Return parameters
        self.npu_param = [Systolic(128, 128, 1536, 1536, 512), Others(2, 2, 1, 1050, 12.8, "WS")]
        self.pim_param = [Systolic(16, 16, 8, 8, 2), Others(2 ,2 ,256 ,1050 ,512 ,"OS")]
        self.dnn_param = []
        self.save_param =[]

        #DNN_parameters
        self.Topology_path = " "
        self.Batch = 32
        self.NPU_dataflow = "WS"
        self.PIM_dataflow = "OS"

        #Save_parameters
        self.PIM_flag = True
        self.Storing_Path = " "

    def read_config_file(self, config_file):
        """ From configuration file, read parameters"""
        config = cp.ConfigParser()
        config.read(config_file)

        #Enter Run name
        section = 'Run_name'
        self.run_name = config.get(section, 'Run_name')

        #In this section, we distribute form factor with two types: Mobile/PC, Server/Supercomputer.
        section = 'Form_Factor'
        self.form_factor = config.get(section, 'Form_Factor')
        if self.form_factor == ('Mobile' or 'PC'):
            self.npu_flag = True
        else:
            self.npu_flag = False

        #In this section, we enter parameters for NPUs.
        section = 'NPU_Parameters'
        npu_sys = Systolic(0,0,0,0,0)
        npu_others = Others(0,0,0,0,0,"")

        npu_sys.input_buffer = config.getint(section, 'NPU_Input_Buffer')
        npu_sys.filter_buffer = config.getint(section, 'NPU_Filter_Buffer')

        npu_others.pod_dimension_row = config.getint(section, 'NPU_Pod_Dimension_Row')
        npu_others.pod_dimension_col = config.getint(section, 'NPU_Pod_Dimension_Col')
        npu_others.number_of_chip = config.getint(section, 'NPU_Number_of_Pod')

        npu_others.clock_frequency = config.getfloat(section, 'NPU_Clock_Frequency')
        npu_others.bandwidth_per_dimm = config.getfloat(section, 'NPU_Total_Bandwidth')

        if self.npu_flag is True:
            throughput = config.getfloat(section, 'NPU_Throughput')
            npu_sys.systolic_row, npu_sys.systolic_col, npu_others.pod_dimension_row, \
            npu_others.pod_dimension_col = self.convert_throughput(throughput, \
            npu_others.pod_dimension_row, npu_others.pod_dimension_col, npu_others.clock_frequency)

        else:
            npu_sys.systolic_row = config.getint(section, 'NPU_Systolic_Row')
            npu_sys.systolic_col = config.getint(section, 'NPU_Systolic_Col')

        #In this section, enter the parameters for PIM units.
        section = 'PIM_Parameters'
        pim_sys = Systolic(0,0,0,0,0)
        pim_others = Others(0,0,0,0,0,"")

        pim_sys.systolic_row = config.getint(section, 'PIM_Systolic_Row')
        pim_sys.systolic_col = config.getint(section, 'PIM_Systolic_Col')
        pim_sys.input_buffer = config.getfloat(section, 'PIM_Input_Buffer')
        pim_sys.filter_buffer = config.getfloat(section, 'PIM_Filter_Buffer')

        pim_others.pod_dimension_row = config.getint(section, 'PIM_Pod_Dimension_Row')
        pim_others.pod_dimension_col = config.getint(section, 'PIM_Pod_Dimension_Col')
        pim_others.clock_frequency = config.getfloat(section, 'PIM_Clock_Frequency')
        pim_others.bandwidth_per_dimm = config.getfloat(section, 'PIM_Bandwidth_per_DIMM')
        chip_per_dimm = config.getint(section, 'Chip_per_DIMM')
        number_of_dimm = config.getint(section, 'NUmber_of_DIMM')

        #In this section, enter the parameters for DNN Models.
        section = 'DNN_Parameters'
        self.topology_path = config.get(section, 'Topology_Path')
        self.batch = config.getint(section, 'Batch')
        self.npu_dataflow = config.get(section, 'NPU_Dataflow')
        self.pim_dataflow = config.get(section, 'PIM_Dataflow')

        #In this section, eneter the parameters for saving results.
        section = 'Save_Parameters'
        self.PIM_Flag = config.getboolean(section, 'PIM_Flag')
        self.Storing_Path = config.get(section, 'Storing_Path')

    def convert_throughput(self, throughput, NPU_Pod_Dimension_Row, NPU_Pod_Dimension_Col, clock_frequency):
        """."""
        #Throughput = 2 * # of pod * clock frequency
        #of pod = Throughput / (2 * clock frequency)

        num_pe = throughput * 1024 /(2 * clock_frequency)
        mul_two = int(round(math.log(num_pe) / math.log(2),0))

        if mul_two % 2 == 0:
            row = pow(2,int(mul_two/2))
            col = pow(2,int(mul_two/2))
        else:
            row = pow(2,int(mul_two/2))
            col = pow(2,int(mul_two/2)+1)
        #For row case
        if row % NPU_Pod_Dimension_Row == 0:
            row_dim =  NPU_Pod_Dimension_Row
            row = int(row / row_dim)
        else:
            print('PIM_Pod_Dimension_Row is set to 1 because NPU_Systolic_Row is not divided with PIM_Pod_Dimension_Row')
            print('----------------------------------------------------------------------------------------------------')
            row_dim = 1

        #For col case
        if col % NPU_Pod_Dimension_Col == 0:
            col_dim = NPU_Pod_Dimension_Col
            col = int(col / col_dim)
        else:
            print('PIM_Pod_Dimension_Col is set to 1 because NPU_Systolic_Col is not divided with PIM_Pod_Dimension_Col')
            print('----------------------------------------------------------------------------------------------------')
            col_dim = 1

        return row, col, row_dim, col_dim

    def get_parameters(self):
        """. """
        pass

        return run_name,form_factor, npu_params, pim_params, dnn_params, save_params

    def GetConfiguration(self, config_file):
        """."""
        self.read_config_file(config_file)

        return self.get_parameters
