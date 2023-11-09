"Python 3.11.5"

class MobileDistribution:
    def __init__(self):
        pass

    def get_distribution_info(self, pim_scaleout, npu_scaleout, stride):
        pim_dataflow = pim_scaleout.scaleup.others.dataflow
        if pim_dataflow == "OS":
            _,_,_ = self.df_pim_os()
        elif pim_dataflow == "WS":
            _,_,_ = self.df_pim_ws()
        elif pim_dataflow == "IS":
            _,_,_ = self.df_pim_is()

        return 1

    def df_pim_os(self):
        pass
    def df_pim_ws(self):
        pass
    def df_pim_is(self):
        pass

    def mobile_distribution(self, npu_input, npu_filter, pim_input, pim_filter, stride):
        pim_dataflow = self.pim_scaleout.scaleup.others.dataflow
        npu_scaleout = self.npu_scaleout
        pim_scaleout = self.pim_scaleout

        runtime1 = 100000000000000
        runtime2 = 100000000000000

        npu_return = [[False, False], [False, False]]
        pim_return = [[False, False], [False, False]]

        #Case1 - WS_OS
        if pim_dataflow == "OS":
            #Case1 - npu/input_col, pim/input_row
            length = npu_input.shape[1]
            for idx in range(1,length):
                pim_scaleout.operand = Operand(pim_input[:idx,:],pim_filter)
                npu_scaleout.operand = Operand(npu_input[idx:,:],npu_filter)
                npu_runtime = self.scaleup_runtime.get_runtime(npu_scaleout.scaleup, npu_scaleout.operand)
                pim_runtime = self.scaleout.scaleout_mobile_runtime(pim_scaleout, stride)
                runtime_temp = max(npu_runtime, pim_runtime)
                if runtime_temp <= runtime1:
                    runtime1 = runtime_temp
                    case1_idx = idx

            #Case2 - npu/filter_col, pim/filter_col
            length = npu_filter.shape[1]
            for idx in range(1,length):
                pim_scaleout.operand = Operand(pim_input,pim_filter[:,:idx])
                npu_scaleout.operand = Operand(npu_input,npu_filter[:,idx:])
                npu_runtime = self.scaleup_runtime.get_runtime(npu_scaleout.scaleup, npu_scaleout.operand)
                pim_runtime = self.scaleout.scaleout_mobile_runtime(pim_scaleout, stride)
                runtime_temp = max(npu_runtime, pim_runtime)
                if runtime_temp < runtime2:
                    runtime2 = runtime_temp
                    case2_idx = idx

            if runtime1 <= runtime2:
                idx = case1_idx
                pim_return[0] = [True, False]
                npu_return[0] = [False, True]
            else:
                idx = case2_idx
                pim_return[1] = [False, True]
                npu_return[1] = [False, True]

        #Case2 - WS_WS
        if pim_dataflow == "WS":
            #Case1 - npu/input_col, pim/input_col
            length = npu_input.shape[1]
            for idx in range(1,length):
                pim_operand = Operand()
                npu_operand = Operand()
                npu_runtime = self.scaleup_runtime.get_runtime(self.npu_scaleout.scaleup, npu_operand)
                pim_runtime = self.scaleup_runtime.get_runtime(self.pim_scaleout.scaleup, pim_operand)
                runtime_temp = max(npu_runtime, pim_runtime)
                if runtime_temp <= runtime1:
                    runtime1 = runtime_temp
                    case1_idx = idx

        #Case2 - npu/filter_col, pim/filter_col
            length = npu_filter.shape[1]
            for idx in range(1,length):
                pim_operand = Operand(pim_input,pim_filter[:,:idx])
                npu_operand = Operand(npu_input,npu_filter[:,idx:])
                npu_runtime = self.scaleup_runtime.get_runtime(self.npu_scaleout.scaleup, npu_operand)
                pim_runtime = self.scaleup_runtime.get_runtime(self.pim_scaleout.scaleup, pim_operand)
                runtime_temp = max(npu_runtime, pim_runtime)
                if runtime_temp < runtime2:
                    runtime2 = runtime_temp
                    case2_idx = idx

            #something for indice

        #Case3 - WS_IS
        if pim_dataflow == "IS":
            pass
        #Case1 - npu/input_col, pim/input_col
        #Case2 - npu/filter_col, pim/filter_col

        return pim_return, npu_return, idx
