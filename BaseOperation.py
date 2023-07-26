import numpy as np

class BaseOperation:
    def get_data_size_no_duplication(self, matrix):
        data = set()
        for row in matrix:
            x = set(row)
            x.discard("[-1,-1,-1]")
            data |= x
        data_size = len(data)
        return data_size

    def get_data_size_with_duplication(self, matrix):
        data_size = sum(1 for row in matrix for item in row if item != "[-1,-1,-1]")
        return data_size

    def get_num_zero_padding(self, matrix):
        data_size = sum(1 for row in matrix for item in row if item == "[-1,-1,-1]")
        return data_size
    
    def input_padding(self, processor, input_operand):
        length = processor[0] - (len(input_operand) % processor[0])
        input_temp = [["[-1,-1,-1]"] * len(input_operand[0]) for _ in range(length)]
        input_operand = np.concatenate((input_operand, input_temp), axis=0)
        return input_operand

    def filter_padding(self, processor, filter_operand):
        length = processor[1] - (len(filter_operand[0]) % processor[1])
        filter_temp = [["[-1,-1,-1]"] * length for _ in range(len(filter_operand))]
        filter_operand = np.concatenate((filter_operand, filter_temp), axis=1)
        return filter_operand

    def skew_input_matrix(self, input_matrix):
        row, col = len(input_matrix), len(input_matrix[0])
        temp = np.full((row, col + row - 1), "[-1,-1,-1]", dtype='U20')
        for i in range(row):
            temp[i, i:i+col] = input_matrix[i]
        return temp

    def skew_filter_matrix(self, filter_matrix):
        row, col = len(filter_matrix), len(filter_matrix[0])
        temp = np.full((col + row - 1, col), "[-1,-1,-1]", dtype='U20')
        for j in range(col):
            temp[j:j+row, j] = filter_matrix[:, j]
        return temp