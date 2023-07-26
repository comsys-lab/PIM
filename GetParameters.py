import math

#input case1 - Mobile and PC - input length = 26
#input length for npu:10 - Throughput, row_dim, col_dim, npu_row, npu_col, input_buffer_size(KB), filter_buffer_size(KB), bandwidth(GB/s), BW_ratio, Frequency(MHz)
#input length for pim:10 - row, col, pu/chip, chip/dram, num_dram, input_buffer_size(KB), filter_buffer_size(KB), bandwidth(GB/s), BW_ratio, Frequency(MHz)
#input length for dnn:4 - topology_path, batch_size, NPU_DF, PIM_DF
#input length for save:2 - only_NPU(bool), saveing_path(str)

#input case2 - Server and Supercomputer - input length = 27
#input length for npu:11 - row, col, row_dim, col_dim, npu_row, npu_col, input_buffer_size(KB), filter_buffer_size(KB), bandwidth(GB/s), BW_ratio, Frequency(MHz)
#input length for pim:10 - row, col, pu/chip, chip/dram, num_dram, input_buffer_size(KB), filter_buffer_size(KB), bandwidth(GB/s), BW_ratio, Frequency(MHz)
#input length for dnn:4 - topology_path, batch_size, NPU_DF, PIM_DF
#input length for save:2 - only_NPU(bool), saveing_path(str)

class GetParameters:
    def get_parameters(self, npu_param, pim_param, dnn_param, save_param):
        npu_param = self.change_data_types(npu_param)
        pim_param = self.change_data_types(pim_param)
        dnn_param = self.change_data_types(dnn_param)

        npu_param = self.change_npu(npu_param)
        pim_param = self.change_pim(pim_param)
        save_param = self.change_save(save_param)

        return npu_param, pim_param, dnn_param, save_param

    def change_data_types(self, lists):
        for i in range(len(lists)):
            try:
                lists[i] = int(lists[i])
            except ValueError:
                try:
                    lists[i] = float(lists[i])
                except ValueError:
                    pass

        return lists

    def change_multiple_two(self, param):
        throughput = param[0]
        row_dim = param[1]
        col_dim = param[2]

        num_pe = round(math.log2(throughput/2))
        row = pow(2, num_pe // 2)
        col = pow(2, num_pe - (num_pe // 2))

        if row % row_dim == 0 and col % col_dim == 0:
            return [int(row/row_dim), int(col/col_dim), row_dim, col_dim]
        else:
            return [row, col, 1, 1]

    def change_npu(self, npu_param):
        length = len(npu_param)
        if length == 7:
            npu_param_f = self.change_multiple_two(npu_param[:3])
            npu_param_r = npu_param[3:]
            npu_param = npu_param_f + npu_param_r

        npu_param[5] *= 1024
        npu_param[6] *= 1024

        return npu_param

    def change_pim(self, pim_param):
        pim_param[5] *= 1024
        pim_param[6] *= 1024

        return pim_param
    
    def change_save(self, save_param):
        save_param[0] = eval(save_param[0])
        save_param[1] = save_param[1] + '/'

        return save_param

    def return_parameters(self, npu_param, pim_param, dnn_param, save_param):
        return self.get_parameters(npu_param, pim_param, dnn_param, save_param)