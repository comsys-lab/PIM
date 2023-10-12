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
            return_dram_access, stall = self.df_os(scaleup, operand, info)
        elif dataflow == "WS":
            return_dram_access, stall = self.df_ws(scaleup, operand, info)
        elif dataflow == "IS":
            return_dram_access, stall = self.df_is(scaleup, operand, info)

        return return_dram_access, stall

    def df_os(self, scaleup, operand, scaleup_info):
        """When dataflow is os."""
        #Initialize return parameters.
        input_dram = 0
        filter_dram = 0
        output_dram = 0
        stall = 0

        #Define parameters.
        systolic = scaleup.systolic
        input_operand = operand.input_operand
        filter_operand = operand.filter_operand
        output_operand = operand.output_operand

        info = scaleup_info[0]
        row_padding = scaleup_info[1]
        col_padding = scaleup_info[2]

        input_matrice = []
        filter_matrice = []
        output_matrice = []
        for row in range(info[0]):
            #Input tiling
            if row != info[0] - 1:
                input_tile = input_operand[row * systolic.row: (row + 1) * systolic.row]
            else:
                input_tile = input_operand[row * systolic.row: ]
            #check padding_row
            row_val = self.base_operation.row_check(systolic, input_tile)
            pad_row = row_padding[row_val]
            input_tile = self.base_operation.skew_input_matrix(self.base_operation.input_padding(systolic, input_tile))

            for col in range(info[1]):
                #Filter tiling
                if col != info[1] - 1:
                    filter_tile = filter_operand[:,col * systolic.col: (col + 1) * systolic.col]
                else:
                    filter_tile = filter_operand[:,col * systolic.col: ]

                #check padding_col
                col_val = self.base_operation.col_check(systolic, filter_tile)
                pad_col = col_padding[col_val]
                filter_tile = self.base_operation.skew_filter_matrix(self.base_operation.filter_padding(systolic, filter_tile))

                #Concatenate input operand
                input_other_padding = np.full((systolic.row, pad_row + pad_col - 1), -1)
                input_one_tile = np.concatenate((input_tile, input_other_padding), axis=1)
                input_matrice.append(input_one_tile)
                out_pad = input_tile.shape[1]
                #Concatenate filter operand
                filter_other_padding = np.full((pad_row + pad_col - 1, systolic.col),-1)
                filter_one_tile = np.concatenate((filter_tile, filter_other_padding), axis=0)
                filter_matrice.append(filter_one_tile)

                output_tile = output_operand[row * pad_row : (row + 1) * pad_row, col * pad_col : (col + 1) * pad_col]
                output_tile = self.base_operation.skew_filter_matrix(self.base_operation.filter_padding(systolic, output_tile))
                output_other_padding = np.full((out_pad, systolic.col), -1)
                output_ont_tile = np.concatenate((output_tile, output_other_padding), axis=0)
                output_matrice.append(output_ont_tile)



        runtime = self.scaleup_runtime.get_runtime(scaleup, operand)

        input_final = np.transpose(np.concatenate(input_matrice,axis=1))
        filter_final = np.concatenate(filter_matrice, axis = 0)
        ouptut_final = np.concatenate(output_matrice, axis = 0)
        print("Making operand matrix completed\n")

        check_count = 0

        buffer1_flag = True
        buffer2_flag = False
        buffer1 = set()
        buffer2 = set()
        size = 785408
        buffer = np.array([-1])
        temp = []
        while check_count < runtime:
            buf = len(buffer)
            one = self.check(input_final[check_count])
            checking = np.union1d(buffer,one)
            if buf + len(one) > size:
                temp.append(check_count)
                buffer = np.array([-1])
                check_count -= 1
            else:
                buffer = checking
            # if (check_count == runtime - 1) and len(buffer) != 0:
            #     temp.append(len(buffer))
            check_count += 1
        df_t= []
        for i in range(1,len(temp)):
            dif = temp[i] - temp[i-1]
            df_t.append(dif)
        print(min(df_t))
        print(temp)
        return_dram_access = [input_dram, filter_dram, output_dram]
        return return_dram_access, stall

    def check(self, operand):
        a = np.unique(operand)
        return a

    def df_ws(self, scaleup, operand, scaleup_info):
        """When dataflow is ws."""
        #Initialize return parameters.
        input_dram = 0
        filter_dram = 0
        output_dram = 0
        stall = 0

        #Define parameters.
        systolic = scaleup.systolic
        input_operand = operand.input_operand
        filter_operand = operand.filter_operand
        output_operand = operand.output_operand

        info = scaleup_info[0]
        row_padding = scaleup_info[1]
        col_padding = scaleup_info[2]

        input_matrice = []
        filter_matrice = []
        output_matrice = []

        for col in range(info[1]):
            for row in range(info[0]):
                if col != info[1] - 1:
                    if row != info[0] - 1:
                        filter_tile = filter_operand[row * row_padding[0]:(row + 1) * row_padding[0] , col * col_padding[0]:(col + 1) *col_padding[0]]
                    else:
                        filter_tile = filter_operand[row * row_padding[0]:,col * col_padding[0]:(col+1)*col_padding[0]]

                else:
                    if row != info[0] - 1:
                        filter_tile = filter_operand[:,:]
                    else:
                        filter_tile = filter_operand[:,:]

                #Filter tiling
                if col != info[1] - 1:
                    filter_tile = filter_operand[col:]
                else:
                    filter_tile = filter_operand[:]
                #Input tiling
                if row != info[0] - 1:
                    input_tile = input_operand[row * systolic.row: (row + 1) * systolic.row]
                else:
                    input_tile = input_operand[row * systolic.row: ]

            #check padding_row
            row_val = self.base_operation.row_check(systolic, input_tile)
            pad_row = row_padding[row_val]
            input_tile = self.base_operation.skew_input_matrix(self.base_operation.input_padding(systolic, input_tile))

        for row in range(info[0]):
            #Input tiling
            if row != info[0] - 1:
                input_tile = input_operand[row * systolic.row: (row + 1) * systolic.row]
            else:
                input_tile = input_operand[row * systolic.row: ]
            #check padding_row
            row_val = self.base_operation.row_check(systolic, input_tile)
            pad_row = row_padding[row_val]
            input_tile = self.base_operation.skew_input_matrix(self.base_operation.input_padding(systolic, input_tile))

            for col in range(info[1]):
                #Filter tiling
                if col != info[1] - 1:
                    filter_tile = filter_operand[:,col * systolic.col: (col + 1) * systolic.col]
                else:
                    filter_tile = filter_operand[:,col * systolic.col: ]

                #check padding_col
                col_val = self.base_operation.col_check(systolic, filter_tile)
                pad_col = col_padding[col_val]
                filter_tile = self.base_operation.skew_filter_matrix(self.base_operation.filter_padding(systolic, filter_tile))

                #Concatenate input operand
                input_other_padding = np.full((systolic.row, pad_row + pad_col - 1), -1)
                input_one_tile = np.concatenate((input_tile, input_other_padding), axis=1)
                input_matrice.append(input_one_tile)
                out_pad = input_tile.shape[1]
                #Concatenate filter operand
                filter_other_padding = np.full((pad_row + pad_col - 1, systolic.col),-1)
                filter_one_tile = np.concatenate((filter_tile, filter_other_padding), axis=0)
                filter_matrice.append(filter_one_tile)

                output_tile = output_operand[row * pad_row : (row + 1) * pad_row, col * pad_col : (col + 1) * pad_col]
                output_tile = self.base_operation.skew_filter_matrix(self.base_operation.filter_padding(systolic, output_tile))
                output_other_padding = np.full((out_pad, systolic.col), -1)
                output_ont_tile = np.concatenate((output_tile, output_other_padding), axis=0)
                output_matrice.append(output_ont_tile)

        input_final = np.transpose(np.array(input_matrice).reshape(systolic.row, -1))
        filter_final = np.array(filter_matrice).reshape(-1, systolic.col)
        ouptut_final = np.array(output_matrice).reshape(-1, systolic.col)
        print("Making operand matrix completed\n")

        return_dram_access = [input_dram, filter_dram, output_dram]

        return return_dram_access, stall

    def df_is(self, scaleup, operand, info):
        """When dataflow is is."""
        #Initialize return parameters.
        input_dram = 0
        filter_dram = 0
        output_dram = 0
        stall = 0

        systolic = scaleup.systolic
        input_operand = operand.input_operand
        filter_operand = operand.filter_operand
        output_operand = operand.output_operand

        input_matrice = []
        filter_matrice = []
        output_matrice = []

        return_dram_access = [input_dram, filter_dram, output_dram]

        return return_dram_access, stall