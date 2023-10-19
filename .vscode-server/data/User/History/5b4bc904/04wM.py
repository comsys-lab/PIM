"Python 3.11.5"
import numpy as np

class MakeInput:
    """Make input operand matrix and return"""
    def __init__(self):
        self.input_operand = np.zeros((1,1), dtype='U20')

    def make_input_matrix(self, topo):
        """Make input matrix"""
        input_matrix = np.array([[[[i, j, k] for k in range(topo[1])] \
                                for j in range(topo[0])] for i in range(topo[4])])

        return input_matrix

    def make_output(self, topo):
        """Return output row and column."""
        output_row = int(np.ceil((topo[0] - topo[2] + topo[6]) / topo[6]))
        output_col = int(np.ceil((topo[1] - topo[3] + topo[6]) / topo[6]))

        return output_row, output_col

    def make_input_operand_os(self, topo):
        """Make input operand matrix."""
        input_matrix = self.make_input_matrix(topo)
        output_row, output_col = self.make_output(topo)
        input_operand_matrix = []

        for row in range(output_row):
            for col in range(output_col):
                one_row = self.make_input_one_row(topo, row, col, input_matrix)
                input_operand_matrix.append(one_row)

        input_operand_matrix = np.array(input_operand_matrix, dtype='U20')
        row = output_row * output_col
        col = topo[2] * topo[3] * topo[4]

        return input_operand_matrix

    def make_input_one_row(self, topo, output_row, output_col, input_matrix):
        """Make one row for input matrix"""
        temp = []
        print(topo)
        for i in range(topo[4]):
            for j in range(topo[2]):
                for k in range(topo[3]):
                    row = output_row * topo[6] + j
                    col = output_col * topo[6] + k
                    if row < topo[0] and col < topo[1]:
                        temp.append(i*1000000000000+j*1000000+k)
                        #temp.append(str(input_matrix[i, row, col]))
                    else: #for zero padding (stride over 1)
                        temp.append(0)

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
