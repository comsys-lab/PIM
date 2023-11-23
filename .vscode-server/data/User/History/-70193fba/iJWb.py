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
        data.discard(0)
        data_size = len(data)

        return data_size

    #Input: np.ndrarray / Return: int
    def get_data_size_with_duplication(self, matrix):
        """Data size with no duplication."""
        data_size = sum(1 for row in matrix for item in row if item != 0)

        return data_size

    def input_padding(self, systolic, input_operand):
        """To adjust the size of the input operand matrix."""
        row_remainder = input_operand.shape[0] % systolic.row
        if row_remainder != 0:
            padding_rows = systolic.row - row_remainder
            padding_matrix = np.full((padding_rows, input_operand.shape[1]), 0, dtype='U20')
            input_operand = np.concatenate((input_operand, padding_matrix), axis=0)

        return input_operand

    def filter_padding(self, systolic, filter_operand):
        """To adjust the size of the filter operand matrix."""
        col_remainder = filter_operand.shape[1] % systolic.col
        if col_remainder != 0:
            padding_cols = systolic.col - col_remainder
            padding_matrix = np.full((filter_operand.shape[0], padding_cols), 0, dtype='U20')
            filter_operand = np.concatenate((filter_operand, padding_matrix), axis=1)

        return filter_operand

    def skew_input_matrix(self, input_operand):
        """Skew input operand matrix."""
        row, col = input_operand.shape
        skewed_matrix = np.full((row, col + row - 1), 0, dtype='U20')

        for i in range(row):
            skewed_matrix[i, i:i+col] = input_operand[i, :]

        return skewed_matrix

    def skew_filter_matrix(self, filter_operand):
        """Skew filter operand matrix."""
        row, col = filter_operand.shape
        skewed_matrix = np.full((col + row - 1, col), 0, dtype='U20')

        for j in range(col):
            skewed_matrix[j:j+row, j] = filter_operand[:, j]

        return skewed_matrix

    def return_os_padding(self, scaleup):
        """Return operand size padding."""
        return scaleup.systolic.row * scaleup.systolic.col

    def others_padding(self, scaleup, row):
        pass

    # #Input: systolic | operand / Return: np.ndarray
    # def input_padding(self, systolic, input_operand):
    #     """To adjust size of input operand matrix."""
    #     length = systolic.row - (input_operand.row % systolic.row)
    #     input_temp = [[0] * input_operand.col for _ in range(length)]
    #     input_operand = np.concatenate((input_operand, input_temp), axis=0)

    #     return input_operand

    # #Input: systolic | operand / Return: np.ndarray
    # def filter_padding(self, systolic, filter_operand):
    #     """To adjust size of filter operand matrix."""
    #     length = systolic.col - (filter_operand.col % systolic.col)
    #     filter_temp = [[0] * length for _ in range(filter_operand.row)]
    #     filter_operand = np.concatenate((filter_operand.systolic, filter_temp), axis=1)

    #     return filter_operand

    # #Input: operand / Return: np.ndarray
    # def skew_input_matrix(self, input_operand):
    #     """Skew input operand matrix."""
    #     row, col = input_operand.row, input_operand.col
    #     input_temp = np.full((row, col + row - 1), 0, dtype='U20')
    #     for i in range(row):
    #         input_temp[i, i:i+col] = input_operand.systolic[i]

    #     return input_temp

    # #Input: operand / Return: np.ndarray
    # def skew_filter_matrix(self, filter_operand):
    #     """Skew filter operand matrix."""
    #     row, col = filter_operand.row, filter_operand.col
    #     temp = np.full((col + row - 1, col), 0, dtype='U20')
    #     for j in range(col):
    #         temp[j:j+row, j] = filter_operand.systolic[:, j]

    #     return temp
