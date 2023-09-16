"Python 3.11.2"

class batch_distribute:
    """"."""
    def batch_distribute(self, npu_proc, pim_proc, dnn_param,  MNK):
        """."""
        batch = dnn_param[1]
        NPU_df = dnn_param[2]
        PIM_df = dnn_param[3]
        npu_result, pim_result = [], [] 

        length = len(MNK)
        for i in range(length):
            NPU_runtime = self.NPU(npu_proc,MNK[i],NPU_df)
            PIM_runtime = self.PIM(pim_proc,MNK[i],PIM_df)

            npu_result.append(NPU_runtime)
            pim_result.append(PIM_runtime)

        return sum(npu_result), sum(pim_result)

    def return_MNK(self, MNK, dataflow):
        if dataflow == "OS":
            return MNK
        elif dataflow == "WS":
            return [MNK[1],MNK[0],MNK[2]]
        elif dataflow == "IS":
            return [MNK[1],MNK[2],MNK[0]]

    def NPU(self, npu_proc, MNK, dataflow):
        if dataflow == "OS":
            npu_runtime = self.OS(npu_proc, MNK)
        elif dataflow == "WS":
            npu_runtime = self.WS(npu_proc, MNK)
        elif dataflow == "IS":
            #npu_runtime = 
            pass
        return npu_runtime
    
    def PIM(self, pim_proc, MNK, dataflow):
        if dataflow == "OS":
            pim_runtime = self.OS(pim_proc, MNK)
        elif dataflow == "WS":
            pim_runtime = self.WS(pim_proc, MNK)
        elif dataflow == "IS":
            #pim_runtime = 
            pass
        return pim_runtime
    
    def OS(self, processor, MNK):
        [SR,SC,T] = self.return_MNK(MNK,"OS")

        row_q = SR // processor[0]
        col_q = SC // processor[1]

        row_rest = (SR % processor[0])
        col_rest = (SC % processor[1])

        row_flag = (SR % processor[0]) != 0
        col_flag = (SC % processor[1]) != 0

        #CASE1
        runtime1 = T + processor[0] + (processor[0] + processor[1] - 2)
        #CASE2
        runtime2 = T + processor[0] + (row_rest + processor[1] - 2)
        #CASE3
        runtime3 = T + processor[0] + (processor[0] + col_rest - 2)
        #CASE4
        runtime4 = T + processor[0] + (row_rest + col_rest - 2)

        runtime = runtime1 * row_q * col_q + runtime2 * row_flag * col_q + runtime3 * row_q * col_flag + runtime4 * row_flag * col_flag

        return runtime

    def WS(self, processor, MNK):
        [SR,SC,T] = self.return_MNK(MNK,"WS")
        row_q = SR // processor[0]
        col_q = SC // processor[1]

        row_rest = (SR % processor[0])
        col_rest = (SC % processor[1])

        row_flag = (SR % processor[0]) != 0
        col_flag = (SC % processor[1]) != 0

        #CASE1
        runtime1 = T + processor[0] - 1 + (processor[0] + processor[1] - 1)
        #CASE2
        runtime2 = T + processor[0] - 1 + (row_rest + processor[1] - 1)
        #CASE3
        runtime3 = T + processor[0] - 1 + (processor[0] + col_rest- 1)
        #CASE4
        runtime4 = T + processor[0] - 1 + (row_rest + col_rest - 1)

        runtime = runtime1 * row_q * col_q + runtime2 * row_flag * col_q + runtime3 * row_q * col_flag + runtime4 * row_flag * col_flag

        return runtime
