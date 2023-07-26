import sys
sys.path.append('/home/sj/simulation/')

from Base.BaseOperation import BaseOperation

class ScaleupSRAM:
    def __init__(self):
        self.BaseOperation = BaseOperation()
        
    def scaleup_sram(self, info, input_operand, filter_operand, dataflow, stride):
        if stride == 1:
            input, filter, output = self.sram_stride_one(info, input_operand, filter_operand, dataflow)
        else:
            input, filter, output = self.sram_stride_over_one(info, input_operand, filter_operand, dataflow)

        return input, filter, output

    def sram_stride_one(self, info, input_operand, filter_operand, dataflow):
        if dataflow == "OS":
            return self.OS_one(info, input_operand, filter_operand)
        elif dataflow == "WS":
            return self.WS_one(info, input_operand, filter_operand)
        elif dataflow == "IS":
            return self.IS_one(info, input_operand, filter_operand)

    def sram_stride_over_one(self, info, input_operand, filter_operand, dataflow):
        if dataflow == "OS":
            return self.OS_over_one(info, input_operand, filter_operand)
        elif dataflow == "WS":
            return self.WS_over_one(info, input_operand, filter_operand)
        elif dataflow == "IS":
            return self.IS_over_one(info, input_operand, filter_operand)

    def calculate_input_size(self, info, input_operand):
        return info[1] * len(input_operand) * len(input_operand[0])

    def calculate_filter_size(self, info, filter_operand):
        return info[0] * len(filter_operand) * len(filter_operand[0])

    def calculate_output_size(self, input_operand, filter_operand):
        return len(input_operand) * len(filter_operand[0])

    def OS_one(self, info, input_operand, filter_operand):
        input = self.calculate_input_size(info, input_operand)
        filter = self.calculate_filter_size(info, filter_operand)
        output = self.calculate_output_size(input_operand, filter_operand)
        return input, filter, output

    def WS_one(self, info, input_operand, filter_operand):
        input = self.calculate_input_size(info, input_operand)
        filter = len(filter_operand) * len(filter_operand[0])
        output = info[0] * len(input_operand[0]) * len(filter_operand[0])
        return input, filter, output

    def IS_one(self, info, input_operand, filter_operand):
        input = len(input_operand) * len(input_operand[0])
        filter = info[1] * len(filter_operand) * len(filter_operand[0])
        output = info[0] * len(input_operand[0]) * len(filter_operand[0])
        return input, filter, output

    def OS_over_one(self, info, input_operand, filter_operand):
        input_operand_size = self.BaseOperation.get_data_size_with_duplication(input_operand)
        filter_operand_size = len(filter_operand) * len(filter_operand[0])

        input = info[1] * input_operand_size
        filter = info[0] * filter_operand_size
        output = len(input_operand) * len(filter_operand[0])
        return input, filter, output

    def WS_over_one(self, info, input_operand, filter_operand):
        input_operand_size = self.BaseOperation.get_data_size_with_duplication(input_operand)
        filter_operand_size = len(filter_operand) * len(filter_operand[0])

        input = info[1] * input_operand_size
        filter = filter_operand_size
        output = info[0] * len(input_operand[0]) * len(filter_operand[0])
        return input, filter, output

    def IS_over_one(self, info, input_operand, filter_operand):
        filter_operand_size = len(filter_operand) * len(filter_operand[0])
        input_operand_size = self.BaseOperation.get_data_size_with_duplication(input_operand)

        input = input_operand_size
        filter = info[1] * filter_operand_size
        output = info[0] * len(filter_operand[0]) * len(input_operand[0])
        return input, filter, output