import numpy as np

class get_batch_case_one:
    def __init__(self):
        pass

    def get_batch_case_one(self,pim_pro,npu_pro,pim_df,npu_df,MNK,check):
        length = len(MNK)
        arr = []
        for i in range(length):
            if check[i]:
                var = MNK[i][0]
            else:
                var = MNK[i][2]
            runtime = 100000000000
            index = 0
            for j in range(1,var):
                pim_runtime = self.pim_runtime_case_one(var-j,pim_pro,pim_df,MNK[i],check[i])
                npu_runtime = self.npu_runtime_case_one(j,npu_pro,npu_df,MNK[i])
                temp = max(pim_runtime,npu_runtime)
                if temp<runtime:
                    runtime = temp
                    index = j
            arr.append([var,index])
        return arr

    #-----------------------------------------------------------------------------------------------------------------------
    def pim_runtime_case_one(self,var,pim_pro,dataflow,MNK,check):
        if check:
            pim_runtime = self.pim_runtime_check_True(var,pim_pro,dataflow,MNK)
        else:
            pim_runtime = self.pim_runtime_check_False(var,pim_pro,dataflow,MNK)

        return pim_runtime
    #-----------------------------------------------------------------------------------------------------------------------
    def pim_runtime_check_True(self,var,pim_pro,dataflow,MNK):
        #input_row>filter_col
        if dataflow == "OS":
            pim_runtime = self.pim_runtime_check_True_OS(var,pim_pro,MNK)
        elif dataflow == "WS":
            pim_runtime = self.pim_runtime_check_True_WS(var,pim_pro,MNK)
        elif dataflow == "IS":
            pim_runtime = self.pim_runtime_check_True_IS(var,pim_pro,MNK)
        
        return pim_runtime
    
    def pim_runtime_check_True_OS(self,var,pim_pro,MNK):
        row = np.ceil(var/pim_pro[2])
        col = np.ceil(MNK[2]/pim_pro[3])

        runtime = (2*pim_pro[0]+pim_pro[1]+MNK[1]-2) * np.ceil(row/pim_pro[0]) * np.ceil(col/pim_pro[1])
        return runtime
    
    def pim_runtime_check_True_WS(self,var,pim_pro,MNK):
        row = np.ceil(MNK[1]/pim_pro[2])
        col = np.ceil(MNK[2]/pim_pro[3])

        runtime = (2*pim_pro[0]+pim_pro[1]+var-2) * np.ceil(row/pim_pro[0]) * np.ceil(col/pim_pro[1])
        return runtime
    
    def pim_runtime_check_True_IS(self,var,pim_pro,MNK):
        pass

    #-----------------------------------------------------------------------------------------------------------------------
    def pim_runtime_check_False(self,var,pim_pro,dataflow,MNK):
        #input_row<filter_col
        if dataflow == "OS":
            pim_runtime = self.pim_runtime_check_False_OS(var,pim_pro,MNK)
        elif dataflow == "WS":
            pim_runtime = self.pim_runtime_check_False_WS(var,pim_pro,MNK)
        elif dataflow == "IS":
            pim_runtime = self.pim_runtime_check_False_IS(var,pim_pro,MNK)

        return pim_runtime
    
    def pim_runtime_check_False_OS(self,var,pim_pro,MNK):
        row = np.ceil(MNK[0]/pim_pro[2])
        col = np.ceil(var/pim_pro[3])

        runtime = (2*pim_pro[0]+pim_pro[1]+MNK[1]-2) * np.ceil(row/pim_pro[0]) * np.ceil(col/pim_pro[1])
        return runtime
    
    def pim_runtime_check_False_WS(self,var,pim_pro,MNK):
        row = np.ceil(MNK[1]/pim_pro[2])
        col = np.ceil(var/pim_pro[3])

        runtime = (2*pim_pro[0]+pim_pro[1]+MNK[0]-2) * np.ceil(row/pim_pro[0]) * np.ceil(col/pim_pro[1])
        return runtime
    
    def pim_runtime_check_False_IS(self,var,pim_pro,MNK):
        pass

    #-----------------------------------------------------------------------------------------------------------------------
    def npu_runtime_case_one(self,var,npu_pro,dataflow,MNK):
        if dataflow == "OS":
            npu_runtime = self.npu_runtime_case_one_OS(var,npu_pro,MNK)
        elif dataflow == "WS":
            npu_runtime = self.npu_runtime_case_one_WS(var,npu_pro,MNK)
        elif dataflow == "IS":
            npu_runtime = self.npu_runtime_case_one_IS(var,npu_pro,MNK)

        return npu_runtime
    
    def npu_runtime_case_one_OS(self,var,npu_pro,MNK):
        row = np.ceil(var/npu_pro[4])
        col = np.ceil(MNK[2]/npu_pro[5])

        runtime = (2*npu_pro[0]+npu_pro[1]+MNK[1]-2) * np.ceil(np.ceil(row/npu_pro[2])/npu_pro[0]) * np.ceil(np.ceil(col/npu_pro[3])/npu_pro[1])
        return runtime
    
    def npu_runtime_case_one_WS(self,var,npu_pro,MNK):
        row = np.ceil(MNK[0]/npu_pro[4])
        col = np.ceil(MNK[2]/npu_pro[5])

        runtime = (2*npu_pro[0]+npu_pro[1]+var-2) * np.ceil(np.ceil(row/npu_pro[2])/npu_pro[0]) * np.ceil(np.ceil(col/npu_pro[3])/npu_pro[1])
        return runtime
    
    def npu_runtime_case_one_IS(self,var,npu_pro,MNK):
        pass