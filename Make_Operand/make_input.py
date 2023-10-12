"Python 3.11.5"
import numpy as np
import time
class MakeInput:
    """Make input operand matrix and return"""
    def __init__(self):
        self.input_operand = np.zeros((1,1), dtype='U20')

    def make_output(self, topo):
        """Return output row and column."""
        output_row = int(np.ceil((topo[0] - topo[2] + topo[6]) / topo[6]))
        output_col = int(np.ceil((topo[1] - topo[3] + topo[6]) / topo[6]))

        return output_row, output_col

    def make_input_operand_os(self, topo):
        """Make input operand matrix."""
        output_row, output_col = self.make_output(topo)
        output_size = output_row * output_col
        input_operand_matrix = []

        for row in range(output_row):
            for col in range(output_col):
                one_row = self.make_input_one_row(topo, row, col, output_size)
                input_operand_matrix.append(one_row)
        input_operand_matrix = np.array(input_operand_matrix, dtype = np.int32)

        return input_operand_matrix

    def make_input_one_row(self, topo, output_row, output_col, output_size):
        """Make one row for input matrix"""
        temp = []
        input_row = topo[0]
        input_col = topo[1]
        filter_row = topo[2]
        filter_col = topo[3]
        channel = topo[4]
        stride = topo[6]
        maximum = len(str(channel))

        for i in range(channel):
            for j in range(filter_row):
                for k in range(filter_col):
                    row = output_row * stride+ j
                    col = output_col * stride+ k
                    if row < input_row and col < input_col:
                        #temp.append(i*10000000000+row*100000+col)
                        if filter_row == 1 and filter_col == 1:
                            temp.append(row*pow(10,maximum)+i)
                        #else:
                        #    temp.append(i*10000000000+row*100000+col)
                    else: #for zero padding (stride over 1)
                        temp.append(-1)
        return temp

    def make_input_operand_ws_is(self, topo):
        """Make input operand matrix for WS and IS dataflow."""
        input_operand = self.make_input_operand_os(topo)
        return_operand = np.transpose(input_operand)

        return return_operand

    def return_input_operand(self, topo, dataflow):
        """Return input operand matrix."""
        if dataflow == "OS":
            input_opearnd = self.make_input_operand_os(topo)
        else:
            input_opearnd = self.make_input_operand_ws_is(topo)

        self.input_operand = input_opearnd

        return self.input_operand
