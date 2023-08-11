import numpy as np
from tqdm import tqdm

from BaseOperation.Baseoperation import BaseOperation

class DramBuffer:
    def __init__(self):
        self.BaseOperation = BaseOperation()

    def dram_buffer(self,processor,info,input_operand,filter_operand,input_buf,filter_buf,dataflow):
        if dataflow == "OS":
            input,filter,output =  self.OS(processor,info,input_operand,filter_operand,input_buf,filter_buf)
        elif dataflow == "WS":
            input,filter,output = self.WS(processor,info,input_operand,filter_operand,input_buf,filter_buf)
        elif dataflow == "IS":
            input,filter,output = self.IS(processor,info,input_operand,filter_operand,input_buf,filter_buf)

        return input,filter,output

    def OS(self,processor,info,input_operand,filter_operand,input_buf,filter_buf):
        input = 0
        filter = 0
        output = len(input_operand) * len(filter_operand[0])

        input_total = [["[-1,-1,-1]"] for i in range(processor[0])]
        filter_total = [["[-1,-1,-1]" for i in range(processor[1])]]

        if len(input_operand)%processor[0] != 0:
            input_operand = self.BaseOperation.input_padding(processor,input_operand)
        if len(filter_operand[0])%processor[1] != 0:
            filter_operand = self.BaseOperation.filter_padding(processor,filter_operand)

        for i in range(info[0]):
            input_tile = self.BaseOperation.skew_input_matrix(input_operand[i*processor[0]:(i+1)*processor[0]])
            for j in range(info[1]):
                input_total = np.concatenate((input_total,input_tile), axis = 1)
        input_total = np.transpose(input_total)
        print("Finish Making Input tiling Matrix",'\n')

        for i in range(info[1]):
            filter_tile = self.BaseOperation.skew_filter_matrix(filter_operand[:,i*processor[1]:(i+1)*processor[1]])
            filter_total = np.concatenate((filter_total,filter_tile), axis = 0)
        print("Finish Making Filter tiling Matrix",'\n')

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

    def WS(self,processor,info,input_operand,filter_operand,input_buf,filter_buf):
        input = 0
        filter = 0
        output = len(input_operand[0]) * len(filter_operand[0])

        input_total = [["[-1,-1,-1]"] for i in range(processor[0])]
        filter_total = [["[-1,-1,-1]" for i in range(processor[1])]]

        if len(input_operand)%processor[0] != 0:
            input_operand = self.BaseOperation.input_padding(processor,input_operand)
        if len(filter_operand[0])%processor[1] != 0:
            filter_operand = self.BaseOperation.filter_padding(processor,filter_operand)

        for i in range(info[0]):
            input_tile = self.BaseOperation.skew_input_matrix(input_operand[i*processor[0]:(i+1)*processor[0]])
            input_total = np.concatenate((input_total,input_tile), axis = 1)
        input_total = np.transpose(input_total)
        print("Finish Making Input tiling Matrix",'\n')

        for i in range(info[1]):
            filter_tile = self.BaseOperation.skew_filter_matrix(filter_operand[:,i*processor[1]:(i+1)*processor[1]])
            filter_total = np.concatenate((filter_total,filter_tile), axis = 0)
        print("Finish Making Filter tiling Matrix",'\n')
        
        #initialize
        print("Calculate Input DRAM access")
        buffer = set()
        input_length = len(input_total)
        
        for i in tqdm(range(info[1])):
            count = 0
            while count<input_length:
                temp = set(np.unique(input_total[count]))
                temp.discard("[-1,-1,-1]")
                if len(buffer|temp) > input_buf:
                    input += len(buffer)
                    count-=1
                    buffer = set()

                else:
                    buffer = buffer|temp
                
                if (i == info[1] - 1) and (count == input_length - 1):
                    input += len(buffer)

                count+=1

        print("Finish calculate Input DRAM access",'\n')
        
        #initialize
        print("Calculate Filter DRAM access")
        
        #Old Version
        buffer = set()
        filter_length = len(filter_total)
        count = 0
        with tqdm(total = filter_length) as pbar:
            while count<filter_length:
                temp = set(np.unique(filter_total[count]))
                temp.discard("[-1,-1,-1]")
                if len(buffer|temp) > filter_buf:
                    filter += len(buffer)
                    count-=1
                    buffer = set()
                else:
                    buffer = buffer|temp
                    pbar.update(1)
                if (count == filter_length - 1):
                    filter += len(buffer)
                
                count += 1
        
        print("Finish calculate Filter DRAM access",'\n')
        return input,filter,output


    def IS(self,processor,info,input_operand,filter_operand,input_buf,filter_buf):
        input = 0
        filter = 0
        output = len(input_operand[0]) * len(filter_operand[0])
        
        filter_total = [["[-1,-1,-1]"] for i in range(processor[0])]
        input_total = [["[-1,-1,-1]" for i in range(processor[1])]]
        #filter and input are exchanged
        if len(filter_operand)%processor[0] != 0:
            filter_operand = self.BaseOperation.input_padding(processor,filter_operand)
        if len(input_operand[0])%processor[1] != 0:
            input_operand = self.BaseOperation.filter_padding(processor,input_operand)


        for i in range(info[0]):
            filter_tile = self.BaseOperation.skew_input_matrix(filter_operand[i*processor[0]:(i+1)*processor[0]])
            filter_total = np.concatenate((filter_total,filter_tile), axis = 1)
        filter_total = np.transpose(filter_total)
        print("Finish Making Filter tiling Matrix")
        

        for i in range(info[1]):
            input_tile = self.BaseOperation.skew_filter_matrix(input_operand[:,i*processor[1]:(i+1)*processor[1]])
            input_total = np.concatenate((input_total,input_tile), axis = 0)
        print("Finish Making Input tiling Matrix")

        #initialize
        print("Calculate Filter DRAM access")
        buffer = set()
        filter_length = len(filter_total)
        
        for i in tqdm(range(info[1])):
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
                
                if (i == info[1] - 1) and (count == filter_length - 1):
                    filter += len(buffer)

                count+=1
            
        print("Finish calculate Filter DRAM access",'\n')

        #initialize
        print("Calculate Input DRAM access")
        buffer = set()
        input_length = len(input_total)
        count = 0
        with tqdm(total = input_length) as pbar:
            while count<input_length:
                temp = set(input_total[count])
                temp.discard('[-1,-1,-1]')
                if len(buffer|temp) > input_buf:
                    input += len(buffer)
                    count -= 1
                    buffer = set()
                else:
                    buffer = buffer|temp
                    pbar.update(1)
                
                if (count == input_length - 1):
                    input += len(buffer)
                
                count += 1

        print("Finish calculate Input DRAM access",'\n')

        return input,filter,output