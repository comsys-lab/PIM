import configparser as cp
import math

class GetConfiguration:
    def __init__(self):
        self.run_name = "run_name"

        #Form_Factor
        self.Form_Factor = "Server"

        #NPU_parameters
        self.Throughput = 16384
        self.Systolic_Row = 128
        self.Systolic_Col = 128
        self.Pod_Dimension_Row = 2
        self.Pod_Dimension_Col = 2
        self.Number_of_Pod = 1
        self.Input_Buffer = 1536
        self.Filter_Buffer = 1536
        self.Clock_Frequency = 1050
        self.Total_Bandwidth = 409.6

        #PIM_parameters
        self.Systolic_Row = 16
        self.Systolic_Col = 16
        self.Pod_Dimension_Row = 2
        self.Pod_Dimension_Col = 2
        self.PU_per_Chip = 4
        self.Chip_per_DIMM = 8
        self.Number_of_DIMM = 32
        self.Input_Buffer = 8
        self.Filter_Buffer = 8
        self.PIM_Bandwidth_per_DIMM = 512

        #DNN_parameters
        self.Topology_path = " "
        self.Batch = 32
        self.NPU_dataflow = "WS"
        self.PIM_dataflow = "OS"

        #Save_parameters
        self.PIM_flag = True
        self.Storing_Path = " "

    def read_config_file(self, config_file):
        
        config = cp.ConfigParser()
        config.read(config_file)
        
        #Enter Run name
        section = 'Run_name'
        self.Run_name = config.get(section, 'Run_name')

        #In this section, we distribute form factor with two types; Mobile and PC (Throughput), Server and Supercomputer.
        section = 'Form_Factor'
        self.Form_Factor = config.get(section, 'Form_Factor')
        if (self.Form_Factor == 'Mobile') or (self.Form_Factor == 'PC'):
            self.NPU_flag = True
        else:
            self.NPU_flag = False

        #In this section, we enter parameters for NPUs.
        section = 'NPU_Parameters'

        self.NPU_Pod_Dimension_Row = config.getint(section, 'NPU_Pod_Dimension_Row')
        self.NPU_Pod_Dimension_Col = config.getint(section, 'NPU_Pod_Dimension_Col')
        self.NPU_Number_of_Pod = config.getint(section, 'NPU_Number_of_Pod')
        self.NPU_Input_Buffer = config.getint(section, 'NPU_Input_Buffer')
        self.NPU_Filter_Buffer = config.getint(section, 'NPU_Filter_Buffer')
        self.NPU_Clock_Frequency = config.getfloat(section, 'NPU_Clock_Frequency')
        self.NPU_Total_Bandwidth = config.getfloat(section, 'NPU_Total_Bandwidth')

        if self.NPU_flag == True:
            self.NPU_Throughput = config.getfloat(section, 'NPU_Throughput')
            self.NPU_Systolic_Row, self.NPU_Systolic_Col, self.NPU_Pod_Dimension_Row, self.NPU_Pod_Dimension_Col\
                  = self.convert_throughput(self.NPU_Throughput, self.NPU_Pod_Dimension_Row, \
                                            self.NPU_Pod_Dimension_Col, self.NPU_Clock_Frequency)
        
        else:
            self.NPU_Systolic_Row = config.getint(section, 'NPU_Systolic_Row')
            self.NPU_Systolic_Col = config.getint(section, 'NPU_Systolic_Col')
        
        #In this section, enter the parameters for PIM units.
        section = 'PIM_Parameters'
        self.PIM_Systolic_Row = config.getint(section, 'PIM_Systolic_Row')
        self.PIM_Systolic_Col = config.getint(section, 'PIM_Systolic_Col')
        self.PIM_Pod_Dimension_Row = config.getint(section, 'PIM_Pod_Dimension_Row')
        self.PIM_Pod_Dimension_Col = config.getint(section, 'PIM_Pod_Dimension_Col')
        self.PU_per_Chip = config.getint(section, 'PU_per_Chip')
        self.Chip_per_DIMM = config.getint(section, 'Chip_per_DIMM')
        self.Number_of_DIMM = config.getint(section, 'NUmber_of_DIMM')
        self.PIM_Input_Buffer = config.getint(section, 'PIM_Input_Buffer')
        self.PIM_Filter_Buffer = config.getint(section, 'PIM_Filter_Buffer')
        self.PIM_Clock_Frequency = config.getint(section, 'PIM_Clock_Frequency')
        self.PIM_Bandwidth_per_DIMM = config.getfloat(section, 'PIM_Bandwidth_per_DIMM')

        #In this section, enter the parameters for DNN Models. 
        section = 'DNN_Parameters'
        self.Topology_Path = config.get(section, 'Topology_Path')
        self.Batch = config.getint(section, 'Batch')
        self.NPU_Dataflow = config.get(section, 'NPU_Dataflow')
        self.PIM_Dataflow = config.get(section, 'PIM_Dataflow')

        #In this section, eneter the parameters for saving results.
        section = 'Save_Parameters'
        self.PIM_Flag = config.getboolean(section, 'PIM_Flag')
        self.Storing_Path = config.get(section, 'Storing_Path')
        
    def convert_throughput(self, throughput, NPU_Pod_Dimension_Row, NPU_Pod_Dimension_Col, clock_frequency):
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
        run_name = self.Run_name
        form_factor = self.Form_Factor
        npu_params = [self.NPU_Systolic_Row, self.NPU_Systolic_Col, self.NPU_Pod_Dimension_Row, \
                            self.NPU_Pod_Dimension_Col, self.NPU_Number_of_Pod, self.NPU_Input_Buffer, \
                            self.NPU_Filter_Buffer, self.NPU_Clock_Frequency, self.NPU_Total_Bandwidth]
        pim_params = [self.PIM_Systolic_Row, self.PIM_Systolic_Col, self.PIM_Pod_Dimension_Row, \
                           self.PIM_Pod_Dimension_Col, self.PU_per_Chip, self.Chip_per_DIMM, \
                            self.Number_of_DIMM, self.PIM_Input_Buffer, self.PIM_Filter_Buffer, \
                                self.PIM_Clock_Frequency, self.PIM_Bandwidth_per_DIMM]
        dnn_params = [self.Topology_Path, self.Batch, self.NPU_Dataflow, self.PIM_Dataflow]
        save_params = [self.PIM_Flag, self.Storing_Path]

        return run_name,form_factor, npu_params, pim_params, dnn_params, save_params
    
    def GetConfiguration(self, config_file):
        self.read_config_file(config_file)
        
        return self.get_parameters