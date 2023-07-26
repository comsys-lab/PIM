import numpy as np
import pandas as pd
import os

from Base.GetParameters import GetParameters as gp
from Base.GetTopology import GetTopology as gt

from Base.get_batch_case_one import get_batch_case_one as gbco
from Base.get_batch_case_over_one import get_batch_case_over_one as gbcoo
from MakeOperand.MakeOperand import MakeOperand as mo
from scaleout.scaleout_bw_ideal import scaleout_bw_ideal as sbi
from batch_distribute import batch_distribute as bd
class simulation:
    def __init__(self):
        self.gp = gp()
        self.gt = gt()
        self.gbco = gbco()
        self.sbi = sbi()
        self.gbcoo = gbcoo()
        self.mo = mo()
        self.bd = bd()

    def simulation(self,npu_param,pim_param,dnn_param,save_param):
        self.get_settings(npu_param,pim_param,dnn_param,save_param)
        temp = ""
        for i in range(8):
            x = str(self.npu_param[i])+"_"
            temp += x

        if not self.save_param[0]:
            name = "NPU_"
        else:
            name =  "PIM_"
            temp += "__"
            for i in range(8):
                temp+=str(self.pim_param[i])+"_"
        
        topo_name = "__"+self.dnn_param[0].split("/")[-1].split(".")[0]
        name += temp+topo_name

        #Case with only NPU -> save_param[0] == False
        #Case with PIM -> save_param[0] == True
        if self.save_param[0]:
            self.with_pim(name)
        else:
            self.only_npu(name)
        

    def get_settings(self,npu_param,pim_param,dnn_param,save_param):
        self.npu_param, self.pim_param, self.dnn_param, self.save_param = self.gp.return_parameters(npu_param,pim_param,dnn_param,save_param)
        self.topology, self.MNK = self.gt.return_topology(self.dnn_param[0])
        self.batch = self.dnn_param[1]

    def only_npu(self,name):

        result = [0,0,0,0,0,0,0,0]
        temp = []
        count = self.npu_param[4]
        info = [self.npu_param + self.dnn_param]
        for i in range(len(self.topology)):
            print('Layer {}'.format(i+1))
            return_info = self.one_layer_only_npu(i)
            temp.append(return_info)
            for i in range(len(return_info)):
                result[i] += return_info[i]

        run_mul = int(np.ceil(self.batch/count))
        mem_mul = self.batch

        for i in range(len(result)):
            result[i] *= mem_mul
        result.append(result[-1] * run_mul)

        temp = info + temp + [result]
        
        string = name
        path = self.save_param[1] + string + '.csv'

        f = open(path,'w')
        f.write("ONLY NPU\n")
        for i in temp:
            f.write(str(i)[1:-1])
            f.write('\n')
        f.close()
                
    def with_pim(self,name):
        NPU_result = [0,0,0,0,0,0,0,0]
        NPU_temp = []
        NPU_info = [self.npu_param+self.dnn_param[:3]]

        PIM_result = [0,0,0,0,0,0,0,0]
        PIM_temp = []
        PIM_info = [self.pim_param + [self.dnn_param[3]]]
        
        for i in range(len(self.topology)):
            print('Layer {}'.format(i+1))
            npu_return = self.one_layer_only_npu(i)
            pim_return = self.one_layer_only_pim(i)

            NPU_temp.append(npu_return)
            PIM_temp.append(pim_return)
            for i in range(len(npu_return)):
                NPU_result[i] += npu_return[i]
                PIM_result[i] += pim_return[i]

        ratio = self.npu_param[7]/self.pim_param[7]
        npu_runtime = NPU_result[-1]
        pim_runtime = int(np.ceil(PIM_result[-1]*ratio))
        
        pim = self.pim_param[3] * self.pim_param[4]
        npu = self.npu_param[4]
        runtime = 1000000000000000000000
        index = 0

        for i in range(1,self.batch):
            runtime_temp = max(int(np.ceil(i/pim))*pim_runtime,int(np.ceil((self.batch-i)/npu))*npu_runtime)
            if runtime_temp<runtime:
                runtime = runtime_temp
                index = i
        pim_batch = index
        npu_batch = self.batch - index
        
        NPU_info[0] += [npu_batch]
        PIM_info[0] += [pim_batch]
        print(NPU_info,PIM_info)
        NPU_temp = NPU_info + NPU_temp + [NPU_result]
        PIM_temp = PIM_info + PIM_temp + [PIM_result]
  
        string = name
        path = self.save_param[1] + string + '.csv'

        f = open(path,'w')
        f.write("WITH PIM\n")
        for i in NPU_temp:
            f.write(str(i)[1:-1])
            f.write('\n')
        f.write('\n')
        for i in PIM_temp:
            f.write(str(i)[1:-1])
            f.write('\n')    
        f.close()

    def one_layer_only_npu(self,index):
        IO,FO,ST = self.mo.return_operand(self.topology[index],self.dnn_param[2])
        return_info = self.sbi.scaleout_bw_ideal(processor = self.npu_param, input_operand = IO, filter_operand = FO, input_buf = self.npu_param[5]/2,\
                                                 filter_buf = self.npu_param[6]/2, dataflow = self.dnn_param[2], stride = ST)

        return return_info
    
    def one_layer_only_pim(self,index):
        IO,FO,ST = self.mo.return_operand(self.topology[index],self.dnn_param[3])
        return_info = self.sbi.scaleout_bw_ideal([self.pim_param[0],self.pim_param[1],1,self.pim_param[2]],IO,FO,self.pim_param[5]/2,self.pim_param[6]/2,\
                                                 self.dnn_param[3],stride = ST)

        return return_info