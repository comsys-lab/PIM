"Python 3.11.5"
import numpy as np

class Baseoperation:
    """Base operation used in scaleup simulation"""
    #Input: np.ndrarray / Return: int
    def get_data_size_no_duplication(self, matrix):
        """Data size with duplication."""
        data = set()
        for row in matrix:
            row = set(row)
            data |= row
        data.discard("[-1,-1,-1]")
        data_size = len(data)

        return data_size

    #Input: np.ndrarray / Return: int
    def get_data_size_with_duplication(self, matrix):
        """Data size with no duplication."""
        data_size = sum(1 for row in matrix for item in row if item != "[-1,-1,-1]")

        return data_size

    #Input: systolic | operand / Return: np.ndarray
    def input_padding(self, systolic, input_operand):
        """To adjust size of input operand matrix."""
        length = systolic.row - (input_operand.row % systolic.row)
        input_temp = [["[-1,-1,-1]"] * input_operand.col for _ in range(length)]
        input_operand = np.concatenate((input_operand, input_temp), axis=0)

        return input_operand

    #Input: systolic | operand / Return: np.ndarray
    def filter_padding(self, systolic, filter_operand):
        """To adjust size of filter operand matrix."""
        length = systolic.col - (filter_operand.col % systolic.col)
        filter_temp = [["[-1,-1,-1]"] * length for _ in range(filter_operand.row)]
        filter_operand = np.concatenate((filter_operand.systolic, filter_temp), axis=1)

        return filter_operand

    #Input: operand / Return: np.ndarray
    def skew_input_matrix(self, input_operand):
        """Skew input operand matrix."""
        row, col = input_operand.row, input_operand.col
        input_temp = np.full((row, col + row - 1), "[-1,-1,-1]", dtype='U20')
        for i in range(row):
            input_temp[i, i:i+col] = input_operand.systolic[i]

        return input_temp

    #Input: operand / Return: np.ndarray
    def skew_filter_matrix(self, filter_operand):
        """Skew filter operand matrix."""
        row, col = filter_operand.row, filter_operand.col
        temp = np.full((col + row - 1, col), "[-1,-1,-1]", dtype='U20')
        for j in range(col):
            temp[j:j+row, j] = filter_operand.systolic[:, j]

        return temp
