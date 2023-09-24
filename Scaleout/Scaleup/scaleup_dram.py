"Python 3.11.5"
import numpy as np

from .base_operation import Baseoperation

class Scaleupdram:
    """Get DRAM access count."""
    def __init__(self):
        self.base_operation = Baseoperation()

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

    def df_os(self, scaleup, operand, info):
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

        #Padding
        input_operand = self.base_operation.input_padding(scaleup.systolic, input_operand)
        filter_operand= self.base_operation.filter_padding(scaleup.systolic, filter_operand)

        input_matrice = []
        for i in range(info[0]):
            input_tile = self.base_operation.skew_input_matrix(input_operand[i * systolic.row: (i + 1) * systolic.row])
            for _ in range(info[1]):
                input_matrice.append(input_tile)
        input_final = np.transpose(np.array(input_matrice).reshape(systolic.row,-1))
        print("Making input tiling matrix completed\n")

        filter_matrice = []
        for i in range(info[1]):
            filter_tile = self.base_operation.skew_filter_matrix(filter_operand[:,i * systolic.col:(i+1) * systolic.col])
            for j in range(info[0]):
                filter_matrice.append(filter_tile)
        filter_total = np.array(filter_matrice).reshape(-1,systolic.col)
        print("Finish Making Filter tiling Matrix",'\n')

        #print(info[0]*info[1]*(systolic.row +9+ (input_total.shape[0]-1)/48))
        print(input_final.shape, filter_total.shape)

        return 1
