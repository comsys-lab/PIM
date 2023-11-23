"Python 3.11.5"
import numpy as np

from .base_operation import Baseoperation
from .scaleup_runtime import Scaleupruntime

class Scaleupdram:
    """Get DRAM access count."""
    def __init__(self):
        self.base_operation = Baseoperation()
        self.scaleup_runtime = Scaleupruntime()

    def scaleup_dram(self, scaleup, operand, info):
        """Get scaleup dram count. Divide case with stride."""
        dataflow = scaleup.others.dataflow
        if dataflow == "OS":
            return_dram_access = self.df_os(scaleup, operand, info)
        # elif dataflow == "WS":
        #     return_dram_access = self.df_ws(scaleup, operand, info)
        # elif dataflow == "IS":
        #     return_dram_access = self.df_is(scaleup, operand, info)

        return return_dram_access

    def df_os(self, scaleup, operand, scaleup_info):
        """When dataflow is os."""
        #Initialize return parameters.
        # input_access = 0
        # filter_access = 0
        # output_access = 0
        # count = 0
        # stall = 0

        #Define parameters.
        systolic = scaleup.systolic
        input_operand = operand.input_operand
        filter_operand = operand.filter_operand
        info = scaleup_info[0]
        row_padding = scaleup_info[1]
        col_padding = scaleup_info[2]

        filter_operand= self.base_operation.filter_padding(systolic, filter_operand)

        input_matrice = []
        filter_matrice = []
        output_matrice = []

        for row in range(info[0]):
            #Input tiling
            if row != info[0] - 1:
                input_tile = input_operand[row * systolic.row: (row + 1) * systolic.row]
            else:
                input_tile = input_operand[row * systolic.row: ]

            row_val = self.base_operation.row_check(systolic, input_tile)
            pad_row = row_padding[row_val]
            input_tile = self.base_operation.skew_input_matrix(self.base_operation.input_padding(systolic, input_tile))

            for col in range(info[1]):
                if col != info[1] - 1:
                    filter_tile = filter_operand[:,col * systolic.col: (col + 1) * systolic.col]
                else:
                    filter_tile = filter_operand[:,col * systolic.col: ]

                col_val = self.base_operation.col_check(systolic, filter_tile)
                pad_col = col_padding[col_val]
                filter_tile = self.base_operation.skew_filter_matrix(self.base_operation.filter_padding(systolic, filter_tile))

                input_other_padding = np.full((systolic.row, pad_row + pad_col - 1), -1)
                input_one_tile = np.concatenate((input_tile, input_other_padding), axis=1)
                input_matrice.append(input_one_tile)

                filter_other_padding = np.full((pad_row + pad_col - 1, systolic.col),-1)
                filter_one_tile = np.concatenate((filter_tile, filter_other_padding), axis=0)
                filter_matrice.append(filter_one_tile)



        input_final = np.transpose(np.array(input_matrice).reshape(systolic.row,-1))
        print("Making input tiling matrix completed\n")

        filter_matrice = []
        for i in range(info[1]):
            for j in range(info[0]):
                filter_tile = self.base_operation.skew_filter_matrix(filter_operand[:,i * systolic.col:(i+1) * systolic.col])
                filter_matrice.append(filter_tile)
        filter_final = np.array(filter_matrice).reshape(-1,systolic.col)
        print("Finish Making Filter tiling Matrix",'\n')

        runtime = self.scaleup_runtime.get_runtime(scaleup, operand)
#        while runtime > 0:
#            pass
        buffer1_flag = True
        buffer2_flag = False
        buffer1 = set()
        buffer2 = set()

        print(input_final.shape, filter_final.shape, runtime)

        return 1

    def df_ws(self, scaleup, operand, info):
        """When dataflow is ws."""
        #Initialize parameters

        systolic = scaleup.systolic
        input_operand = operand.input_operand
        filter_operand = operand.filter_operand

        input_operand = self.base_operation.input_padding(systolic, input_operand)

        #Input with WS dataflow, iterate one input operand matrix.
        for col in range(info[1]):
            if col != info[1] - 1:
                input_tile = self.base_operation.skew_input_matrix(input_operand[row * systolic.row: (row + 1) * systolic.row])
            else:
                input_tile = self.base_operation.skew_input_matrix(input_operand[:, row * systolic.row: ])
            for row in range(info[0]):
                if row != info[0] - 1:
                    pass
                else:
                    pass

        for row in range(info[0]):
            if row != info[0] - 1:
                input_tile = self.base_operation.skew_input_matrix(input_operand[row * systolic.row: (row + 1) * systolic.row])
                return_row_flag = False
            else:
                input_tile = self.base_operation.skew_input_matrix(input_operand[row * systolic.row: ])
                return_row_flag = True
            for col in range(info[1]):
                if col != info[1] - 1:
                    return_col_flag = False
                else:
                    return_col_flag = True
                [pad_one, pad_two] = padding_info[return_col_flag][return_row_flag]
                input_padding = np.full((systolic.row, pad_one + pad_two - 1), -1)
                if row_return_flag == False:
                    input_tile = self.base_operation.input_padding(scaleup.systolic, input_tile)
                input_matrice.append(input_tile)
                input_matrice.append(input_padding)

        return 1

    def df_is(self, scaleup, operand, info):
        """When dataflow is is."""
        #Initialize parameters
        systolic = scaleup.systolic
        input_operand = operand.input_operand
        filter_operand = operand.filter_operand

        input_matrice = []

        return 1