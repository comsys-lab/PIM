import configparser as cp

class config:
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
        
        config = cp.configparser()
        config.read(config_file)

        section = 'Form_Factor'
        self.Form_Factor = config.get(section, 'Form_Factor')
        if self.Form_Factor == ('Mobile' or 'PC'):
            self.flag = True
        else:
            self.flag = False

        section = 'NPU_Parameters'
        self.Throughput = float(config.get(section, 'Throuhgput'))
        self.Systolic_Row = int(config.get(section, 'Systolic_Row'))
        self.Systolic_Col = int(config.get(section, 'Systolic_Col'))
        self.Pod_Dimension_Row = int(config.get(section, 'Pod_Dimension_Row'))
        self.Pod_Dimension_Col = int(config.get(section, 'Pod_Dimension_Col'))
        self.Number_of_Pod = int(config.get(section, 'Number_of_Pod'))
        self.Input_Buffer = int(config.get(section, 'Input_Buffer'))
        self.Filter_Buffer = int(config.get(section, 'Filter_Buffer'))
        self.Clock_Frequency = int(config.get(section, 'Clock_Frequency'))
        self.Total_Bandwidth = float(config.get(section, 'Total_Bandwidth'))

        section = 'PIM_Parameters'
        self.Systolic_Row = int(config.get(section, 'Systolic_Row'))
        self.Systolic_Col = int(config.get(section, 'Systolic_Col'))
        self.Pod_Dimension_Row = int(config.get(section, 'Pod_Dimension_Row'))
        self.Pod_Dimension_Col = int(config.get(section, 'Pod_Dimension_Col'))
        self.PU_per_Chip = int(config.get(section, 'PU_per_Chip'))
        self.Chip_per_DIMM = int(config.get(section, 'Chip_per_DIMM'))
        self.Number_of_DIMM = int(config.get(section, 'NUmber_of_DIMM'))
        self.Input_Buffer = int(config.get(section, 'Input_Buffer'))
        self.Filter_Buffer = int(config.get(section, 'Filter_Buffer'))
        self.PIM_Bandwidth_per_DIMM = float(config.get(section, 'PIM_Bandwidth_per_DIMM'))

        section = 'DNN_Parameters'
        self.Topology_Path = config.get(section, 'Topology_Path')
        self.Batch = int(config.get(section, 'Batch'))
        self.NPU_Dataflow = config.get(section, 'NPU_Dataflow')
        self.PIM_Dataflow = config.get(section, 'PIM_Dataflow')

        section = 'Save_parameters'
        self.PIM_Flag = eval(config.get(section, 'PIM_Flag'))
        self.Storing_Path = int(config.get(section, 'Storing_Path'))

    def return_parameters(self):
        self.npu_params = []
        self.pim_params = []
        self.dnn_params = []
        self.save_params = []

    def convert_params(self):
        