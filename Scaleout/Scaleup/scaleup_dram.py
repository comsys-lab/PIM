"Python 3.11.5"
import numpy as np

from .base_operation import Baseoperation
from .scaleup_runtime import Scaleupruntime
from .base_class import Operand

class Scaleupdram:
    """Get DRAM access count."""
    def __init__(self):
        self.base_operation = Baseoperation()
        self.scaleup_runtime = Scaleupruntime()

    def scaleup_dram(self, scaleup, operand, info):
        """Get scaleup dram count. Divide case with stride."""
        dataflow = scaleup.others.dataflow
        if dataflow == "OS":
            input_dram, filter_dram, output_dram, stall = self.df_os(scaleup, operand, info)
        elif dataflow == "WS":
            input_dram, filter_dram, output_dram, stall = self.df_ws(scaleup, operand, info)
        elif dataflow == "IS":
            input_dram, filter_dram, output_dram, stall = self.df_is(scaleup, operand, info)

        return input_dram, filter_dram, output_dram, stall

    def df_os(self, scaleup, operand, scaleup_info):
        """When dataflow is os."""
        #Initialize return parameters.
        input_dram_access = 0
        filter_dram_access = 0
        output_dram_access = operand.input_operand.shape[0] * operand.filter_operand.shape[1]

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
        input_buffer_size = scaleup.systolic.input_buffer * 512
        filter_buffer_size = scaleup.systolic.filter_buffer * 512

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

        stall = self.check_stall(input_check, filter_check, scaleup, operand)

        return input_dram_access, filter_dram_access, output_dram_access, stall

    def df_ws(self, scaleup, operand, scaleup_info):
        """When dataflow is ws."""
        #Initialize return parameters.
        input_dram_access = 0
        filter_dram_access = 0
        output_dram_access = operand.input_operand.shape[1] * operand.filter_operand.shape[1]

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
        input_buffer_size = scaleup.systolic.input_buffer * 512
        filter_buffer_size = scaleup.systolic.filter_buffer * 512

        for col in range(info[1]):
            for row in range(info[0]):
                #Input tiling
                if row != info[0] - 1:
                    input_tile = input_operand[row * systolic.row : (row + 1) * systolic.row]
                else:
                    input_tile = input_operand[row * systolic.row : ]
                #check padding_row
                row_val = self.base_operation.row_check(systolic, input_tile)
                pad_row = row_padding[row_val]
                input_tile = self.base_operation.skew_input_matrix(self.base_operation.input_padding(systolic, input_tile))

                #Filter tiling
                if col != info[1] - 1:
                    filter_tile = filter_operand[:,col * systolic.col : (col + 1) * systolic.col]
                else:
                    filter_tile = filter_operand[:,col * systolic.col : ]
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

                length = filter_one_tile.shape[0]

                filter_length_counter = 0
                while filter_length_counter < length:
                    filter_checking = np.union1d(filter_buffer,filter_one_tile[filter_length_counter])
                    if filter_checking[0] == -1:
                        filter_checking = filter_checking[1:]
                    filter_temp = filter_checking.size

                    if filter_temp > filter_buffer_size:
                        filter_dram_access += len(filter_buffer)
                        count_now = count+filter_length_counter+1
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

        stall = self.check_stall(input_check, filter_check, scaleup, operand)

        return input_dram_access, filter_dram_access, output_dram_access, stall

    def df_is(self, scaleup, operand, info):
        """When dataflow is is."""
        operand_temp = Operand(None, None)
        operand_temp.input_operand = operand.filter_operand
        operand_temp.filter_operand = operand.input_operand
        filter_dram_access, input_dram_access, output_dram_access, stall = self.df_ws(scaleup, operand_temp, info)

        return input_dram_access, filter_dram_access, output_dram_access, stall

    def check_stall(self, input_check, filter_check, scaleup, operand):
        """Check stall."""
        runtime = self.scaleup_runtime.get_runtime(scaleup, operand)
        latency = scaleup.others.latency
        bandwidth = scaleup.others.bandwidth
        input_size = operand.input_operand.shape[0] * operand.input_operand.shape[1]
        filter_size = operand.filter_operand.shape[0] * operand.filter_operand.shape[1]

        input_fill1 = False
        input_fill2 = True

        input_use1 = True
        input_use2 = False

        input_buf_size = scaleup.systolic.input_buffer * 512
        input_fill = -1 * latency * bandwidth

        input_stall_flag = False

        filter_fill1 = False
        filter_fill2 = True

        filter_use1 = True
        filter_use2 = False

        filter_buf_size = scaleup.systolic.filter_buffer * 512
        filter_fill = -1 * latency * bandwidth

        filter_stall_flag = False

        count = 0
        stall = int(np.ceil(max(min(input_size,input_buf_size),min(filter_size,filter_buf_size))/bandwidth))

        input_counter = 0
        filter_counter = 0

        while count < runtime:
            if len(input_check) != 0:
                input_stall_count = input_check[input_counter]
                #Using case ->change flags
                if count == input_stall_count:
                    if input_counter <= len(input_check) - 2:
                        input_counter += 1

                    if input_use1:
                        input_use1 = False
                        input_use2 = True
                    else:
                        input_use1 = True
                        input_use2 = False

                #If we can fill, just fill the buffer
                if input_fill1 or input_fill2:
                    input_fill += bandwidth

                #if buffer is full, change filling flags
                if input_fill >= input_buf_size:
                    input_fill = -1 * latency * bandwidth
                    if input_fill1:
                        if input_use2:
                            input_fill1 = False
                            input_fill2 = False
                        else:
                            input_fill1 = False
                            input_fill2 = True
                    if input_fill2:
                        if input_use1:
                            input_fill1 = False
                            input_fill2 = False
                        else:
                            input_fill1 = True
                            input_fill2 = False

            #check input stall
            if (input_fill1 == True and input_use1 == True) or (input_fill2 == True and input_use2 == True):
                input_stall_flag = True
            else:
                input_stall_flag = False

            #

            if len(filter_check) != 0:
                filter_stall_count = filter_check[filter_counter]
                #Using case ->change flags
                if count == filter_stall_count:
                    if filter_counter <= len(filter_check) - 2:
                        filter_counter += 1

                    if filter_use1:
                        filter_use1 = False
                        filter_use2 = True
                        filter_fill1 = True
                    else:
                        filter_use1 = True
                        filter_use2 = False
                        filter_fill2 = True

                #If we can fill, just fill the buffer
                if filter_fill1 or filter_fill2:
                    filter_fill += bandwidth

                #if buffer is full, change filling flags
                if filter_fill >= filter_buf_size:
                    filter_fill = -1 * latency * bandwidth
                    if filter_fill1:
                        if filter_use2:
                            filter_fill1 = False
                            filter_fill2 = False
                        else:
                            filter_fill1 = False
                            filter_fill2 = True
                    if filter_fill2:
                        if filter_use1:
                            filter_fill1 = False
                            filter_fill2 = False
                        else:
                            filter_fill1 = True
                            filter_fill2 = False

            #check filter stall
            if (filter_fill == True and filter_use1 == True) or (filter_fill2 == True and filter_use2 == True):
                filter_stall_flag = True
            else:
                filter_stall_flag = False

            if input_stall_flag or filter_stall_flag:
                stall += 1
            else:
                count += 1

        return stall
