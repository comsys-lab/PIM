"Python 3.10.8"
from base_operation import Baseoperation

class Scaleupsram:
    """Get SRAM access count."""
    def __init__(self):
        self.base_operation = Baseoperation()

    def scaleupsram(self, params, stride):
        """Get scaleup sram count. Divide case with stride."""
        if stride == 1:
            return_sram_access = self.sram_stride_one(params)
        else:
            return_sram_access = self.sram_stride_over_one(params)

        return return_sram_access

    #Layer with stride 1 doesn't have duplication data in input operand matrix.
    def sram_stride_one(self, params):
        """Get SRAM access count when stride is one."""
        dataflow_functions = {
            "OS": self.os_one,
            "WS": self.ws_one,
            "IS": self.is_one
        }

        dataflow_function = dataflow_functions.get(params.dataflow)
        if dataflow_function:
            return_sram_access = dataflow_function(params)
        else:
            raise ValueError("Invalid dataflow value")

        return return_sram_access

    #Calculate input and filter SRAM access count.
    def return_sram_access_count_stride_one(self, params):
        """."""
        input_size, filter_size = self.return_matrix_size(params)
        input_access_count = params.num_col_tiles

        return_sram_access = [0,0,0]
        return return_sram_access
    def return_matrix_size(self, params):
        """."""
        if params.dataflow == "IS":
            input_size = 1
            filter_size = 1
        else:
            input_size = 1
            filter_size =1

        return input_size, filter_size

    def return_input_stride_one(self, Num_Col_Tiles, Input_Operand):
        return Num_Col_Tiles * len(Input_Operand) * len(Input_Operand[0])

    def Return_Filter_Access_Count_Stride_One(self, Num_Row_Tiles, Filter_Operand):
        return Num_Row_Tiles * len(Filter_Operand) * len(Filter_Operand[0])

    def Return_Output_Access_Count_Stride_Oned(self, Input_Operand, Filter_Operand):
        return len(Input_Operand) * len(Filter_Operand[0])

    def os_one(self, params):
        input_access, filter_access, output_access = self.return_sram_access_count_stride_one(params)

        return_sram_access = [input_access,filter_access, output_access]

        return return_sram_access

    def ws_one(self, params):
        input_access = self.return_sram_access_count_stride_one(params)
        filter_access = self.return_sram_access_count_stride_one(params)
        output_access = sel
        return_sram_access = [input_access, filter_access, output_access]

        return return_sram_access

    def is_one(self, info, Input_Operand, Filter_Operand):
        input = len(Input_Operand) * len(Input_Operand[0])
        filter = info[1] * len(Filter_Operand) * len(Filter_Operand[0])
        output = info[0] * len(Input_Operand[0]) * len(Filter_Operand[0])

        return return_sram_access
    #--------------------------------------------------------------------------------------------------------
    #Layer with stride over 1 (especially in CNN models) has duplication data input operand matrix.
    def sram_stride_over_one(self, params):
        """Return SRAM access count when stride is one."""
        dataflow_functions = {
            "OS": self.OS_Over_One,
            "WS": self.WS_Over_One,
            "IS": self.IS_Over_One
        }

        dataflow_function = dataflow_functions.get(dataflow)
        if dataflow_function:
            return dataflow_function(Num_Row_Tiles, Num_Col_Tiles, Input_Operand, Filter_Operand)
        else:
            raise ValueError("Invalid dataflow value")

    def return_data_size(self, input_operand, filter_operand):
        """Return data size from input and filter operand matrix."""
        input_data_size = self.base_operation._get_data_size_no_duplication(input_operand)
        filter_data_size = self.base_operation._get_data_size_no_duplication(filter_operand)
        output_data_size = self.base_operation._get_data_size_no_duplication()

        return [input_data_size, filter_data_size, output_data_size]

    def OS_Over_One(self, info, Input_Operand, Filter_Operand):
        input_operand_size, filter_operand_size = self.BaseOperation.get_data_Size_with_duplication(Input_Operand)
        Filter_Operand_Size = len(Filter_Operand) * len(Filter_Operand[0])

        input = info[1] * input_operand_size
        filter = info[0] * filter_operand_size
        output = len(Input_Operand) * len(Filter_Operand[0])
        return input, filter, output

    def WS_Over_One(self, info, Input_Operand, Filter_Operand):
        Input_Operand_Size = self.BaseOperation.get_data_Size_with_duplication(Input_Operand)
        Filter_Operand_Size = len(Filter_Operand) * len(Filter_Operand[0])

        input = info[1] * Input_Operand_Size
        filter = Filter_Operand_Size
        output = info[0] * len(Input_Operand[0]) * len(Filter_Operand[0])
        return input, filter, output

    def IS_Over_One(self, info, Input_Operand, Filter_Operand):
        Filter_Operand_Size = len(Filter_Operand) * len(Filter_Operand[0])
        Input_Operand_Size = self.BaseOperation.get_data_Size_with_duplication(Input_Operand)

        input = Input_Operand_Size
        filter = info[1] * Filter_Operand_Size
        output = info[0] * len(Filter_Operand[0]) * len(Input_Operand[0])
        return input, filter, output