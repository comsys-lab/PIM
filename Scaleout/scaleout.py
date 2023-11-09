"Python 3.11.5"
import numpy as np

from .Scaleup.base_class import Operand
from .Scaleup.base_class import Results

from .Scaleup.scaleup import ScaleUp

class ScaleOut:
    """Scaleout simulation"""
    def __init__(self) -> None:
        self.scaleup = ScaleUp()

    def scaleout(self, scaleout, stride, layer_info):
        dataflow = scaleout.scaleup.others.dataflow
        if dataflow == "OS":
            result = self.scaleout_os(scaleout, stride, layer_info)
        elif dataflow == "WS":
            result = self.scaleout_ws(scaleout, stride, layer_info)
        elif dataflow == "IS":
            result = self.scaleout_is(scaleout, stride, layer_info)

        return result

    def scaleout_os(self, scaleout, stride, layer_info):
        """Scaleout Operation function."""
        print('Scaleout Start layer {}/{}\n'.format(layer_info[0] + 1, layer_info[1]))
        row_info, col_info, energy_info = self.scaleout_info(scaleout)

        scaleup = scaleout.scaleup
        operand = scaleout.operand
        row_dim, col_dim = scaleout.row_dim, scaleout.col_dim
        row_var, col_var = 1, 1

        #Initialize parameters
        result_list = []
        ene_eff = energy_info[0] * energy_info[1]

        #Iteration check
        row_flag, col_flag = self.iteration_check(scaleout, scaleout.operand)
        if stride != 1:
            row_flag = False

        row,col = 0,0
        while row < row_info[0]:
            while col < col_info[0]:
                if row != row_info[0] - 1:
                    input_tile = scaleout.operand.input_operand[row * row_info[1] : (row + 1) * row_info[1]]
                else:
                    input_tile = scaleout.operand.input_operand[row * row_info[1]: ]

                if col != col_info[0] - 1:
                    filter_tile = scaleout.operand.filter_operand[:, col * col_info[1] : (col + 1) * col_info[1]]
                else:
                    filter_tile = scaleout.operand.filter_operand[:, col * col_info[1] : ]

                operand = Operand(input_tile, filter_tile)
                results = self.scaleup.scale_up(scaleup, operand, stride)
                result_list.append(results)

                if col_flag == True:
                    col = col_info[0]
                    col_var = col_dim
                else:
                    col += 1
            if row_flag == True:
                row = row_info[0]
                row_var = row_dim
            else:
                row += 1

        result = self.return_results(result_list, row_var, col_var)
        result.enery_eff = ene_eff

        print('Scaleout End layer {}/{}\n'.format(layer_info[0] + 1, layer_info[1]))

        return result

    def scaleout_ws(self, scaleout, stride, layer_info):
        """Scaleout function for OS dataflow."""
        print('Scaleout Start layer {}/{}\n'.format(layer_info[0] + 1, layer_info[1]))
        row_info, col_info, energy_info = self.scaleout_info(scaleout)

        scaleup = scaleout.scaleup
        operand = scaleout.operand
        row_dim, col_dim = scaleout.row_dim, scaleout.col_dim
        row_var, col_var = 1, 1

        #Initialize parameters
        result_list = []
        ene_eff = energy_info[0] * energy_info[1]

        #Iteration check
        row_flag, col_flag = self.iteration_check(scaleout, scaleout.operand)
        if stride != 1:
            row_flag = False

        row,col = 0,0
        while row < row_info[0]:
            while col < col_info[0]:
                if row != row_info[0] - 1:
                    input_tile = scaleout.operand.input_operand[ : , row * row_info[1] : (row + 1) * row_info[1]]
                else:
                    input_tile = scaleout.operand.input_operand[ : , row * row_info[1]: ]

                if col != col_info[0] - 1:
                    filter_tile = scaleout.operand.filter_operand[ : , col * col_info[1] : (col + 1) * col_info[1]]
                else:
                    filter_tile = scaleout.operand.filter_operand[ : , col * col_info[1] : ]

                operand = Operand(input_tile, filter_tile)
                results = self.scaleup.scale_up(scaleup, operand, stride)
                result_list.append(results)

                if col_flag == True:
                    col = col_info[0]
                    col_var = col_dim
                else:
                    col += 1
            if row_flag == True:
                row = row_info[0]
                row_var = row_dim
            else:
                row += 1

        result = self.return_results(result_list, row_var, col_var)
        result.enery_eff = ene_eff

        print('Scaleout End layer {}/{}\n'.format(layer_info[0] + 1, layer_info[1]))

        return result

    def scaleout_is(self, scaleout, stride, layer_info):
        """Scaleout function for IS dataflow."""
        input_temp = scaleout.operand.input_operand
        filter_temp = scaleout.operand.filter_operand

        scaleout_new = scaleout
        scaleout_new.operand.input_operand = filter_temp
        scaleout_new.operand.filter_operand = input_temp

        result = self.scaleout_ws(scaleout_new, stride, layer_info)

        filter_sram = result.input_sram
        input_sram = result.filter_sram
        result.input_sram = input_sram
        result.filter_sram = filter_sram

        filter_dram = result.input_dram
        input_dram = result.filter_dram
        result.input_dram = input_dram
        result.filter_dram = filter_dram

        return result

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
        row_flag = (row % row_dim) == 0
        col_flag = (col % col_dim) == 0

        return row_flag, col_flag

    def dimension_info(self, scaleout):
        """Return dimension information of each dataflow"""
        dataflow = scaleout.scaleup.others.dataflow
        operand = scaleout.operand

        if dataflow == "OS":
            row, col = operand.input_operand.shape[0], operand.filter_operand.shape[1]
        elif dataflow == "WS":
            row, col = operand.input_operand.shape[1], operand.filter_operand.shape[1]
        elif dataflow == "IS":
            row, col = operand.filter_operand.shape[0], operand.input_operand.shape[1]

        return row, col

    def return_results(self, result_list, row_var, col_var):
        """Collect results from scaleup"""
        results = Results(0,0,0,0,0,0,0,0)
        for result in result_list:
            results.input_sram += result.input_sram * row_var * col_var
            results.filter_sram += result.filter_sram * row_var * col_var
            results.output_sram += result.output_sram * row_var * col_var
            results.input_dram += result.input_dram * row_var * col_var
            results.filter_dram += result.filter_dram * row_var * col_var
            results.output_dram += result.output_dram * row_var * col_var
            results.runtime = max(results.runtime,result.runtime)

        return results

    def scaleout_mobile_runtime(self, scaleout, stride):
        dataflow = scaleout.scaleup.others.dataflow
        if dataflow == "OS":
            runtime = self.mobile_os(scaleout, stride)
        elif dataflow == "WS":
            runtime = self.mobile_ws(scaleout, stride)
        elif dataflow == "IS":
            runtime = self.mobile_is(scaleout, stride)

        return runtime

    def mobile_os(self, scaleout, stride):
        """Scaleout Operation function."""
        row_info, col_info, energy_info = self.scaleout_info(scaleout)

        scaleup = scaleout.scaleup
        operand = scaleout.operand
        row_dim, col_dim = scaleout.row_dim, scaleout.col_dim
        row_var, col_var = 1, 1

        #Iteration check
        row_flag, col_flag = self.iteration_check(scaleout, scaleout.operand)

        if stride != 1:
            row_flag = False

        runtime = 0
        row,col = 0,0
        while row < row_info[0]:
            while col < col_info[0]:
                if row != row_info[0] - 1:
                    input_tile = scaleout.operand.input_operand[row * row_info[1] : (row + 1) * row_info[1]]
                else:
                    input_tile = scaleout.operand.input_operand[row * row_info[1]: ]

                if col != col_info[0] - 1:
                    filter_tile = scaleout.operand.filter_operand[:, col * col_info[1] : (col + 1) * col_info[1]]
                else:
                    filter_tile = scaleout.operand.filter_operand[:, col * col_info[1] : ]

                operand = Operand(input_tile, filter_tile)
                runtime_temp = self.scaleup.scaleup_mobile(scaleup, operand)
                runtime += runtime_temp


                if col_flag == True:
                    col = col_info[0]
                    col_var = col_dim
                else:
                    col += 1
            if row_flag == True:
                row = row_info[0]
                row_var = row_dim
            else:
                row += 1


        runtime *= row_var * col_var

        return runtime

    def mobile_ws(self, scaleout, stride):
        """Scaleout function for OS dataflow."""
        row_info, col_info, energy_info = self.scaleout_info(scaleout)

        scaleup = scaleout.scaleup
        operand = scaleout.operand
        row_dim, col_dim = scaleout.row_dim, scaleout.col_dim
        row_var, col_var = 1, 1

        #Iteration check
        row_flag, col_flag = self.iteration_check(scaleout, scaleout.operand)
        if stride != 1:
            row_flag = False

        runtime = 0
        row,col = 0,0
        while row < row_info[0]:
            while col < col_info[0]:
                if row != row_info[0] - 1:
                    input_tile = scaleout.operand.input_operand[ : , row * row_info[1] : (row + 1) * row_info[1]]
                else:
                    input_tile = scaleout.operand.input_operand[ : , row * row_info[1]: ]

                if col != col_info[0] - 1:
                    filter_tile = scaleout.operand.filter_operand[ : , col * col_info[1] : (col + 1) * col_info[1]]
                else:
                    filter_tile = scaleout.operand.filter_operand[ : , col * col_info[1] : ]

                operand = Operand(input_tile, filter_tile)
                runtime_temp = self.scaleup.scale_up(scaleup, operand, stride)
                runtime += runtime_temp

                if col_flag == True:
                    col = col_info[0]
                    col_var = col_dim
                else:
                    col += 1
            if row_flag == True:
                row = row_info[0]
                row_var = row_dim
            else:
                row += 1
        runtime *= row_var * col_var

        return runtime

    def mobile_is(self, scaleout, stride):
        """Scaleout function for IS dataflow."""
        input_temp = scaleout.operand.input_operand
        filter_temp = scaleout.operand.filter_operand

        scaleout_new = scaleout
        scaleout_new.operand.input_operand = filter_temp
        scaleout_new.operand.filter_operand = input_temp

        runtime = self.mobile_ws(scaleout_new, stride)

        return runtime