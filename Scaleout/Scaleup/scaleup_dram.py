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
        input_dram_access = 0
        filter_dram_access = 0
        output_dram_access = operand.input_operand.shape[0] * operand.filter_operand.shape[1]
        stall = 0

        #Define parameters.
        systolic = scaleup.systolic
        input_operand = operand.input_operand
        filter_operand = operand.filter_operand

        info = scaleup_info[0]
        row_padding = scaleup_info[1]
        col_padding = scaleup_info[2]

        input_buffer = np.array([],dtype=np.int32)
        filter_buffer = np.array([],dtype=np.int32)

        input_check=[]
        filter_check = []

        input_stall_check = 10000000
        filter_stall_check = 10000000

        count = 0
        input_buffer_size = scaleup.systolic.input_buffer
        filter_buffer_size = scaleup.systolic.filter_buffer

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
                input_one_tile = np.transpose(np.concatenate((input_tile, input_other_padding), axis=1))

                #Concatenate filter operand
                filter_other_padding = np.full((pad_row + pad_col - 1, systolic.col),-1)
                filter_one_tile = np.concatenate((filter_tile, filter_other_padding), axis=0)

                length = input_one_tile.shape[0]

                input_length_counter = 0
                while input_length_counter < length:
                    input_checking = np.union1d(input_buffer,input_one_tile[input_length_counter])
                    if input_checking[0] == -1:
                        input_checking = input_checking[1:]
                    input_temp = input_checking.size

                    if input_temp > input_buffer_size:
                        input_dram_access += len(input_buffer)
                        count_now = count+input_length_counter+1
                        if len(input_check) != 0:
                            input_stall_check = min(input_stall_check, count_now - input_check[0])
                        input_check.append(count_now)
                        input_buffer = np.array([],dtype=np.int32)
                        input_length_counter -= 1
                    else:
                        input_buffer = input_checking

                    input_length_counter += 1

                filter_length_counter = 0
                while filter_length_counter < length:
                    filter_checking = np.union1d(filter_buffer,filter_one_tile[filter_length_counter])
                    if filter_checking[0] == -1:
                        filter_checking = filter_checking[1:]
                    filter_temp = filter_checking.size

                    if filter_temp > filter_buffer_size:
                        filter_dram_access += len(filter_buffer)
                        count_now = count+input_length_counter+1
                        if len(filter_check) != 0:
                            filter_stall_check = min(filter_stall_check, count_now - filter_check[0])
                        filter_check.append(count_now)
                        filter_buffer = np.array([],dtype=np.int32)
                        filter_length_counter -= 1
                    else:
                        filter_buffer = filter_checking

                    filter_length_counter += 1

                count += length


        if input_buffer.size != 0:
            if input_dram_access == 0:
                input_dram_access = input_buffer.size
                input_stall_check = 0
            else:
                input_dram_access += len(input_buffer)
        if filter_buffer.size != 0:
            if filter_dram_access == 0:
                filter_dram_access = filter_buffer.size
                filter_stall_check = 0
            else:
                filter_dram_access += len(filter_buffer)


        #fucntion for stall
        runtime = self.scaleup_runtime.get_runtime(scaleup, operand)
        # if input_stall_check <





        return_dram_access = [input_dram_access, filter_dram_access, output_dram_access]
        return return_dram_access, stall

    def df_ws(self, scaleup, operand, scaleup_info):
        """When dataflow is ws."""
        #Initialize return parameters.
        input_dram = 0
        filter_dram = 0
        output_dram = operand.input_operand.shape[0] * operand.filter_operand.shape[1]
        stall = 0

        #Define parameters.
        systolic = scaleup.systolic
        input_operand = operand.input_operand
        filter_operand = operand.filter_operand

        info = scaleup_info[0]
        row_padding = scaleup_info[1]
        col_padding = scaleup_info[2]

        input_buffer = np.array([],dtype=np.int32)
        filter_buffer = np.array([],dtype=np.int32)

        input_check=[]
        filter_check = []

        count = 0
        input_dram_access = 0
        filter_dram_access = 0

        for col in range(info[1]):
            if col != info[1] - 1:
                filter_temp = filter_operand[:,col * systolic.col : (col + 1) * systolic.col]
            else:
                filter_temp = filter_operand[:,col * systolic.col : ]
            for row in range(info[0]):
                if row != info[0] - 1:
                    filter_tile = filter_temp[row * systolic.row : (row + 1),:]
                    input_tile = input_operand[row * systolic.row : (row + 1),:]
                else:
                    filter_tile = filter_temp[row :,:]
                    input_tile = input_operand[row * systolic.row :, : ]

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

    def check_stall(self, input_check, filter_check, input_buffer_size, filter_buffer_size, input_bandwidth, filter_bandwidth, runtime):
        """Check stall."""
        stall = 0

        input_stall_flag = False
        filter_stall_flag = False

        input_buffer1_flag = True
        input_buffer2_flag = False

        filter_buffer1_flag = True
        filter_buffer2_flag = False

        input_filling = input_buffer_size / input_bandwidth
        filter_filling = filter_buffer_size / filter_bandwidth

        input_buffer_check = 0
        filter_buffer_check = 0

        for i in range(runtime):
            pass