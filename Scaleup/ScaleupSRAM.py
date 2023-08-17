"Python 3.10.8"
from base_operation import Baseoperation

class Scaleupsram:
    """Get SRAM access count."""
    def __init__(self):
        self.base_operation = Baseoperation()

    def scaleupsram(self, num_row_tiles, num_col_tiles, input_operand, filter_operand, dataflow, stride):
        """."""
        if stride == 1:
            input_access, filter_access, output = self.sram_stride_one(num_row_tiles, num_col_tiles, Input_Operand, Filter_Operand, dataflow)
        else:
            input, filter, output = self.sram_stride_over_one(Num_Row_Tiles, Num_Col_Tiles, Input_Operand, Filter_Operand, dataflow)

        return input, filter, output

    #Layer with stride 1 doesn't have duplication data in input operand matrix.
    def sram_stride_one(self, Num_Row_Tiles, Num_Col_Tiles, Input_Operand, Filter_Operand, dataflow):
        """."""
        dataflow_functions = {
            "OS": self.OS_One,
            "WS": self.WS_One,
            "IS": self.IS_One
        }

        dataflow_function = dataflow_functions.get(dataflow)
        if dataflow_function:
            return dataflow_function(Num_Row_Tiles, Num_Col_Tiles, Input_Operand, Filter_Operand)
        else:
            raise ValueError("Invalid dataflow value")

    #Calculate input and filter SRAM access count.
    def Return_Input_Access_Count_Stride_One(self, Num_Col_Tiles, Input_Operand):
        return Num_Col_Tiles * len(Input_Operand) * len(Input_Operand[0])

    def Return_Filter_Access_Count_Stride_One(self, Num_Row_Tiles, Filter_Operand):
        return Num_Row_Tiles * len(Filter_Operand) * len(Filter_Operand[0])

    def Return_Output_Access_Count_Stride_Oned(self, Input_Operand, Filter_Operand):
        return len(Input_Operand) * len(Filter_Operand[0])

    def OS_One(self, Num_, Input_Operand, Filter_Operand):
        Input = self.Return_Input_Access_Count_Stride_One(info, Input_Operand)
        Filter = self.Return_Filter_Access_Count_Stride_One(info, Filter_Operand)
        Output = self.Return_Output_Access_Count_Stride_Oned(Input_Operand, Filter_Operand)

        return Input, Filter, Output

    def WS_One(self, info, Input_Operand, Filter_Operand):
        input = self.calculate_input_Size(info, Input_Operand)
        filter = len(Filter_Operand) * len(Filter_Operand[0])
        output = info[0] * len(Input_Operand[0]) * len(Filter_Operand[0])
        return input, filter, output

    def IS_One(self, info, Input_Operand, Filter_Operand):
        input = len(Input_Operand) * len(Input_Operand[0])
        filter = info[1] * len(Filter_Operand) * len(Filter_Operand[0])
        output = info[0] * len(Input_Operand[0]) * len(Filter_Operand[0])
        return input, filter, output

    #Layer with stride over 1 (especially in CNN models) has duplication data input operand matrix.
    def SRAM_Stride_Over_One(self, Num_Row_Tiles, Num_Col_Tiles, Input_Operand, Filter_Operand, dataflow):
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

    def Return_Data_Size(self, Input_Operand, Filter_Operand):

        input_data_size = self.BaseOperation.get_data_size_with_duplication()

        return input_data_size, filter_data_size
    def Return_Input_Size(self, Input_Operand, Filter_Operand):
        pass

    def Return_Filter_Size(self, Input_Operand, Filter_Operand):
        pass
    def OS_Over_One(self, info, Input_Operand, Filter_Operand):
        Input_Operand_Size = self.BaseOperation.get_data_Size_with_duplication(Input_Operand)
        Filter_Operand_Size = len(Filter_Operand) * len(Filter_Operand[0])

        input = info[1] * Input_Operand_Size
        filter = info[0] * Filter_Operand_Size
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