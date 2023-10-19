"Python 3.11.5"
import numpy as np

from .Scaleup.base_class import Operand

from .Scaleup.scaleup import ScaleUp

class ScaleOut:
    """."""
    def __init__(self) -> None:
        self.scaleup = ScaleUp()

    def scaleout(self, scaleout, stride, layer_info):
        dataflow = scaleout.scaleup.others.dataflow
        if dataflow == "OS":
            sram_info, dram_info, runtime, ene_eff = self.scaleout_os(scaleout, stride, layer_info)
        elif dataflow == "WS":
            sram_info, dram_info, runtime, ene_eff = self.scaleout_ws(scaleout, stride, layer_info)
        elif dataflow == "IS":
            sram_info, dram_info, runtime, ene_eff = self.scaleout_is(scaleout, stride, layer_info)

        return sram_info, dram_info, runtime, ene_eff

    def dimension_info(self, scaleout):
        """Return dimension information of each dataflow"""
        dataflow = scaleout.scaleup.others.dataflow
        operand = scaleout.operand

        if dataflow == "IS":
            row, col = operand.filter_operand.shape[0], operand.input_operand.shape[1]
        else:
            row, col = operand.input_operand.shape[0], operand.filter_operand.shape[1]

        return row, col

    def scaleout_info(self, scaleout):
        """Return scaleout information,"""
        row_dim, col_dim = scaleout.row_dim, scaleout.col_dim
        row, col = self.dimension_info(scaleout)
        row_count = min(row, row_dim)
        col_count = min(col, col_dim)
        per_row = int(np.ceil(row / row_count))
        per_col = int(np.ceil(col / col_count))

        row_ene_eff = row / row_dim if row <= row_dim else 1
        col_ene_eff = col / col_dim if col <= col_dim else 1

        return [row_count, per_row], [col_count, per_col], [row_ene_eff, col_ene_eff]

    def iteration_check(self, scaleout, operand):
        """To reduce total runtime of simulation."""
        dataflow = scaleout.scaleup.others.dataflow
        row, col = self.dimension_info(scaleout)

        row_dim, col_dim = scaleout.row_dim, scaleout.col_dim
        row_flag = (row_dim % row) == 0
        col_flag = (col_dim % col) == 0

        return row_flag, col_flag

    def scaleout_os(self, scaleout, stride, layer_info):
        """Scaleout function for OS dataflow."""
        print('Scaleout Start layer {}/{}\n'.format(layer_info[0] + 1, layer_info[1]))
        row_info, col_info, energy_info = self.scaleout_info(scaleout)

        scaleup = scaleout.scaleup

        sram_store = []
        dram_store = []
        runtime_store = []
        #Energy efficiency for unused chips
        ene_eff = energy_info[0] * energy_info[1]

        #check for iteration
        row_flag, col_flag = self.iteration_check(scaleout, scaleout.operand)
        if stride == 1:
            if row_flag == 1 and col_flag:
                pass #This case, we have to simulate only once.

        else:
            pass
        last_row = (row_info[0] - 1) * row_info[1]
        last_col = (col_info[0] - 1) * col_info[1]

        #four cases - 1,2,3,4.

        #black box for scaleout function
        for row in range(row_info[0]):
            if row != row_info[0] - 1:
                input_tile = scaleout.operand.input_operand[row * row_info[1] : (row + 1) * row_info[1]]
            else:
                input_tile = scaleout.operand.input_operand[row * row_info[1]: ]

            for col in range(col_info[0]):
                if col != col_info[0] - 1:
                    filter_tile = scaleout.operand.filter_operand[:, col * col_info[1] : (col + 1) * col_info[1]]
                else:
                    filter_tile = scaleout.operand.filter_operand[:, col * col_info[1] : ]

                operand = Operand(input_tile, filter_tile)

                sram_info, dram_info, runtime = self.scaleup.scale_up(scaleup, operand, stride)
                sram_store.append(sram_info)
                dram_store.append(dram_info)
                runtime_store.append(runtime)


        #Memory access
        sram_info = self.return_memory(sram_store)
        dram_info = self.return_memory(dram_store)
        #Runtime
        runtime = self.return_runtime(runtime_store)

        print('Scaleout End layer {}/{}\n'.format(layer_info[0] + 1, layer_info[1]))
        return sram_info, dram_info, runtime, ene_eff

    def _scaleout_ws(self, scaleout, stride):
        """When dataflow is WS, scaleout function."""
        print('Scaleout Start\n')
        row_info, col_info, energy_info = self.scaleout_info(scaleout)

        scaleup = scaleout.scaleup

        sram_store = []
        dram_store = []
        runtime_store = []
        ene_eff = energy_info[0] * energy_info[1]



    def return_memory(self, memory_store):
        """Return total memory access of each memory."""
        input_access = 0
        filter_access = 0
        output_access = 0

        for access in memory_store:
            input_access += access[0]
            filter_access += access[1]
            output_access += access[2]

        return [input_access, filter_access, output_access]

    def return_runtime(self, runtime_store):
        """Return runtime in scaleout function."""
        return max(runtime_store)
