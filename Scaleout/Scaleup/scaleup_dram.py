"Python 3.11.5"
import numpy as np

from base_operation import Baseoperation

class Scaleup_dram:
    """Get DRAM access count."""
    def __init__(self):
        self.base_operation = Baseoperation()

    def scaleup_dram(self, scaleup, operand, stride):
        """Get scaleup dram count. Divide case with stride."""
        dataflow = scaleup.others.dataflow
        if dataflow == "OS":
            return_dram_access = self.df_os(scaleup, operand, stride)
        elif dataflow == "WS":
            return_dram_access = self.df_ws(scaleup, operand, stride)
        elif dataflow == "IS":
            return_dram_access = self.df_is(scaleup, operand, stride)

        return return_dram_access
    #what about bandwidth and latency?



        return return_dram_access

    def make_input_1d(self, input_operand):
        pass

    def make_filter_1d(self, filter_operand):
        pass

    def df_ws(self, scaleup, operand, stride):
        """When dataflow is ws."""
        if stride == 1:
            pass
        else:
            pass

        return 1

    def df_is(self, scaleup, operand, stride):
        """When dataflow is is."""
        if stride == 1:
            pass
        else:
            pass

        return 1

    def df_os(self, scaleup, operand, info):
        """When dataflow is os."""
        #Initialize return parameters.
        input_access = 0
        filter_access = 0
        output_access = 0
        count = 0
        stall = 0

        input_total = [["[-1,-1,-1]"] for i in range(scaleup.systolic.row)]
        filter_total = [["[-1,-1,-1]" for i in range(scaleup.systolic.col)]]

        systolic = scaleup.systolic
        input_operand = operand.input_operand
        filter_operand = operand.filter_operand

        if operand.input_operand.shape[0] % scaleup.systolic.row != 0:
            input_operand = self.base_operation.input_padding(scaleup.systolic, input_operand)
        if operand.filter_operand.shape[1] % scaleup.systolic.col != 0:
            filter_operand= self.base_operation.filter_padding(scaleup.systolic, filter_operand)

        for i in range(info[0]):
            input_tile = self.BaseOperation.skew_input_matrix(input_operand[i * systolic.row: (i + 1) * systolic.row])
            input_total.append(input_tile)
        input_total = np.transpose(np.concatenate(input_total, axis=1))
        print("Making input tiling matrix completed")

        for i in range(info[1]):
            filter_tile = self.base_operation.skew_filter_matrix(filter_operand[i * systolic.col: (i + 1) * systolic.col])
            filter_total.append(filter_tile)
        filter_total = np.concatenate(filter_total, axis=0)

        print("Calculate Input DRAM access")
        input_buffer = set()
        input_length = input_total.shape[1]
        input_access = 0
        stall = 0

        while count < input_length:
            pass

        return_dram_access = [input_access, filter_access, output_access]
        return return_dram_access, stall

    def df_ws(self, scaleup, operand):

        #initialize
        print("Calculate Input DRAM access")
        buffer = set()
        input_length = len(input_total)
        count = 0

        with tqdm(total = input_length) as pbar:
            while count<input_length:
                temp = set(np.unique(input_total[count]))
                temp.discard("[-1,-1,-1]")
                if len(buffer|temp) > input_buf:
                    input += len(buffer)
                    count-=1
                    buffer = set()
                else:
                    buffer = buffer|temp
                    pbar.update(1)
                
                if (i == info[1] - 1) and (count == input_length - 1):
                    input += len(buffer)
                
                count+=1
            
        print("Finish calculate Input DRAM access",'\n')

        #initialize
        print("Calculate Filter DRAM access")
        buffer = set()
        filter_length = len(filter_total)

        for i in range(info[0]):
            count = 0
            while count<filter_length:
                temp = set(np.unique(filter_total[count]))
                temp.discard("[-1,-1,-1]")
                if len(buffer|temp) > filter_buf:
                    filter += len(buffer)
                    count-=1
                    buffer = set()
                else:
                    buffer = buffer|temp

                if (i == info[0] - 1) and (count == filter_length - 1):
                    filter += len(buffer)

                count+=1

        print("Finish calculate Filter DRAM access",'\n')

        return input,filter,output
