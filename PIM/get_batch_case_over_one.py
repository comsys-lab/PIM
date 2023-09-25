import numpy as np
import sys
sys.path.append('/home/sj/simulation/')

from Base.GetParameters import GetParameters as gp
from Base.GetTopology import GetTopology as gt


class get_batch_case_over_one:
    def __init__(self):
        self.gp = gp()
        self.gt = gt()

    def get_batch_case_over_one(self,pim_pro,npu_pro,batch,pim_fr,npu_fr,pim_df,npu_df,MNK,check):
        runtime = 10000000000000000000000000
        for i in range(1,batch):
            PIM_runtime = self.get_pim_runtime(pim_pro,i,MNK,pim_df,check)
            NPU_runtime = self.get_npu_runtime(npu_pro,batch-i,MNK,npu_df)
            ratio = npu_fr/pim_fr
            temp_runtime = max(PIM_runtime[0]*ratio,NPU_runtime[0])
            if temp_runtime <= runtime:
                runtime = temp_runtime
                return_info = [i,PIM_runtime[1:],NPU_runtime[1]] 

        return return_info
    
    def get_pim_runtime(self,pim_pro,batch,MNK,dataflow,check):
        #each - # of DRAM, #of Chips/DRAM, #of PU/Chips
        Num_D = pim_pro[4]
        Num_CD = pim_pro[3]
        Num_PC = pim_pro[2]

        row = pim_pro[0]
        col = pim_pro[1]

        X = Num_CD * Num_D
        Y = Num_PC * Num_CD

    
        X1 = np.ceil(batch/X)
        if X>batch:
            X1 = batch
            Y1 = 0
        else:
            X1 = (batch//X)*X
            Y1 = batch - X1
            

                    
        temp_runtime = 0
        for x in range(len(MNK)):
            if dataflow == "OS":
                return_info = self.get_pim_runtime_OS(row,col,Num_PC,Num_CD,Num_D,MNK[x],check)
            elif dataflow == "WS":
                return_info = self.get_pim_runtime_WS(row,col,Num_PC,Num_CD,Num_D,MNK[x],check)
            elif dataflow == "IS":
                return_info = self.get_pim_runtime_IS(row,col,Num_PC,Num_CD,Num_D,MNK[x],check)

            temp_runtime += X1/X * return_info[0][0] + np.ceil(Y1/Y) * return_info[1][0]


        total_result = [temp_runtime,[X,X1,return_info[0][1]],[Y,Y1,return_info[1][1]]]

        return total_result
        
    def get_pim_runtime_OS(self,row,col,Num_PC,Num_CD,Num_D,MNK,check):

        if check:
            x1 = 1
            x2 = Num_PC
            if Num_PC>Num_CD:
                x4 = Num_PC
                x3 = Num_CD
            else:
                x3 = Num_PC
                x4 = Num_CD
        else:
            x2 = 1
            x1 = Num_PC            
            if Num_PC>Num_CD:
                x3 = Num_PC
                x4 = Num_CD
            else:
                x4 = Num_PC
                x3 = Num_CD

        case1_runtime = (2*row+col+MNK[1]-2)*np.ceil(np.ceil(MNK[0]/x1)/row) * np.ceil(np.ceil(MNK[2]/x2)/col)
        case2_runtime = (2*row+col+MNK[1]-2)*np.ceil(np.ceil(MNK[0]/x3)/row) * np.ceil(np.ceil(MNK[2]/x4)/col)

        return_info = [[case1_runtime,[row,col,x1,x2]] ,[case2_runtime,[row,col,x3,x4]]]

        return return_info
    
    def get_pim_runtime_WS(self,row,col,Num_PC,Num_CD,Num_D,MNK,check):

        if check:
            x1 = 1
            x2 = Num_PC
            if Num_PC>Num_CD:
                x4 = Num_PC
                x3 = Num_CD
            else:
                x3 = Num_PC
                x4 = Num_CD
        else:
            x2 = 1
            x1 = Num_PC            
            if Num_PC>Num_CD:
                x3 = Num_PC
                x4 = Num_CD
            else:
                x4 = Num_PC
                x3 = Num_CD

        case1_runtime = (2*row+col+MNK[0]-2)*np.ceil(np.ceil(MNK[1]/x1)/row) * np.ceil(np.ceil(MNK[2]/x2)/col)
        case2_runtime = (2*row+col+MNK[0]-2)*np.ceil(np.ceil(MNK[1]/x3)/row) * np.ceil(np.ceil(MNK[2]/x4)/col)

        return_info = [[case1_runtime,[row,col,x1,x2]] ,[case2_runtime,[row,col,x3,x4]]]
        
        return return_info

    def get_pim_runtime_IS(self,row,col,Num_PC,Num_CD,Num_D,MNK,check):

        if check:
            x1 = 1
            x2 = Num_PC
            if Num_PC>Num_CD:
                x4 = Num_PC
                x3 = Num_CD
            else:
                x3 = Num_PC
                x4 = Num_CD
        else:
            x2 = 1
            x1 = Num_PC            
            if Num_PC>Num_CD:
                x3 = Num_PC
                x4 = Num_CD
            else:
                x4 = Num_PC
                x3 = Num_CD
        case1_runtime = (2*row+col+MNK[2]-2)*np.ceil(np.ceil(MNK[1]/x1)/row) * np.ceil(np.ceil(MNK[0]/x2)/col)
        case2_runtime = (2*row+col+MNK[2]-2)*np.ceil(np.ceil(MNK[1]/x3)/row) * np.ceil(np.ceil(MNK[0]/x4)/col)

        return_info = [[case1_runtime,[row,col,x1,x2]] ,[case2_runtime,[row,col,x3,x4]]]
        
        return return_info

    def get_npu_runtime(self,npu_pro,batch,MNK,dataflow):

        npu_pod = npu_pro[4]*npu_pro[5]
        runtime_temp = 0
        for i in range(len(MNK)):
            if dataflow == "OS":
                runtime = self.get_npu_runtime_OS(npu_pro,MNK[i])
            elif dataflow == "WS":
                runtime = self.get_npu_runtime_WS(npu_pro,MNK[i])
            elif dataflow == "IS":
                runtime = self.get_npu_runtime_IS(npu_pro,MNK[i])

            
            runtime_temp += np.ceil(batch/npu_pod) * runtime
        
        return [runtime_temp,[npu_pod,batch,[npu_pro[0],npu_pro[1],npu_pro[2],npu_pro[3]]]]


    def get_npu_runtime_OS(self,npu_pro,MNK):
        case1_runtime = (2*npu_pro[0]+npu_pro[1]+MNK[1]-2) * np.ceil(np.ceil(MNK[0]/npu_pro[2])/npu_pro[0]) * np.ceil(np.ceil(MNK[2]/npu_pro[3])/npu_pro[1])
        
        return case1_runtime
    
    def get_npu_runtime_WS(self,npu_pro,MNK):
        case1_runtime = (2*npu_pro[0]+npu_pro[1]+MNK[0]-2) * np.ceil(np.ceil(MNK[1]/npu_pro[2])/npu_pro[0]) * np.ceil(np.ceil(MNK[2]/npu_pro[3])/npu_pro[1])
        
        return case1_runtime

    def get_npu_runtime_IS(self,npu_pro,MNK):
        case1_runtime = (2*npu_pro[0]+npu_pro[1]+MNK[2]-2) * np.ceil(np.ceil(MNK[1]/npu_pro[2])/npu_pro[0]) * np.ceil(np.ceil(MNK[0]/npu_pro[3])/npu_pro[1])
        
        return case1_runtime

