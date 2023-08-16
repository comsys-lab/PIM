"Python 3.10.8"
import numpy as np

class Baseoperation:
    """Store functions that will be reused in simulator."""
    def get_data_size_no_duplication(self, matrix):
        """
        If dnn layer has stride more than one, then it does zero padding.
        zero padding data = [-1,-1,-1], and simulator use this function when get the sram access.
        """
        data = set()
        for row in matrix:
            row = set(row)
            data |= row
        data.discard("[-1,-1,-1]")
        data_size = len(data)

        return data_size

    def get_data_size_with_duplication(self, matrix):
        """
        If dnn layer has stride more than one, then it does zero padding.
        zero padding data = [-1,-1,-1], and simulator use this function when get the dram access.
        """
        data_size = sum(1 for row in matrix for item in row if item != "[-1,-1,-1]")

        return data_size

    def get_num_zero_padding(self, matrix):
        """Function that number of zeros in the operand matrix."""
        data_size = sum(1 for row in matrix for item in row if item == "[-1,-1,-1]")

        return data_size

    def input_padding(self, systolic, input_operand):
        """
        Dimension of operand matrix is not always divisibe with dimension of systolic array.
        Thus, padding needs to satisfy divisible dimension.
        In the case of input operation matrix, padding should proceed in the row direction.
        """
        length = systolic.row - (len(input_operand) % systolic.row)
        input_temp = [["[-1,-1,-1]"] * len(input_operand[0]) for _ in range(length)]
        input_operand = np.concatenate((input_operand, input_temp), axis=0)

        return input_operand

    def filter_padding(self, systolic, filter_operand):
        """
        Dimension of operand matrix is not always divisibe with dimension of systolic array.
        Thus, padding needs to satisfy divisible dimension.
        In the case of filter operation matrix, padding should proceed in the column direction.
        """
        length = systolic.col - (len(filter_operand[0]) % systolic.col)
        filter_temp = [["[-1,-1,-1]"] * length for _ in range(len(filter_operand))]
        filter_operand = np.concatenate((filter_operand, filter_temp), axis=1)

        return filter_operand

    def skew_input_matrix(self, input_matrix):
        """
        Input operand matrix is skewed in direction of row when the dataflow is OS.
        """
        row, col = len(input_matrix), len(input_matrix[0])
        temp = np.full((row, col + row - 1), "[-1,-1,-1]", dtype='U20')
        for i in range(row):
            temp[i, i:i+col] = input_matrix[i]

        return temp

    def skew_filter_matrix(self, filter_matrix):
        """
        Filter operand matrix is skewed in direction of column when the dataflow is WS and IS.
        """
        row, col = len(filter_matrix), len(filter_matrix[0])
        temp = np.full((col + row - 1, col), "[-1,-1,-1]", dtype='U20')
        for j in range(col):
            temp[j:j+row, j] = filter_matrix[:, j]

        return temp
