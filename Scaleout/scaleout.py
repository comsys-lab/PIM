"Python 3.11.5"
import numpy as np

from .Scaleup.scaleup_class import Scaleup
from .Scaleup.scaleup_class import Operand
from .scaleout_class import Scaleout

from .Scaleup.scaleup_class import Systolic

from .Scaleup.scaleup import ScaleUp

class ScaleOut:
    """."""
    def __init__(self) -> None:
        self.scaleup = ScaleUp()

    def scaleout(self):
        pass

    def dimension_info(self, scaleout):
        dataflow = scaleout.scaleup.others.dataflow
        operand = scaleout.operand

        if dataflow == "OS":
            row, col = operand.input_operand.row, operand.filter_operand.col
        elif dataflow == "WS":
            row, col = operand.input_operand.col, operand.filter_operand.col
        elif dataflow == "IS":
            row, col = operand.filter_operand.row, operand.input_operand.col

        return row, col

    def scaleout_info(self, scaleout):
        """."""
        row_dim, col_dim = scaleout.row_dim, scaleout.col_dim
        row, col = self.dimension_info(scaleout)
        row_count = min(row, row_dim)
        col_count = min(col, col_dim)
        per_row = int(np.ceil(row / row_count))
        per_col = int(np.ceil(col / col_count))

        row_ene_eff = row / row_dim if row <= row_dim else 1
        col_ene_eff = col / col_dim if col <= col_dim else 1


        return [[row_count, per_row], [col_count, per_col], [row_ene_eff, col_ene_eff]]

    def scaleout_os(self, scaleout, scaleoutinfo):
        print('SCALEOUT START\n')
        row_info = scaleoutinfo[0]
        col_info = scaleoutinfo[1]
        ene_info = scaleoutinfo[2]

        result = []

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

                systolic = scaleout.scaleup.systolic
                operand = Operand(input_tile, filter_tile)

            scaleup = ScaleUp(systolic, operand)

            return_temp = self.scaleup.scale_up(scaleup)
            result_temp.append(return_temp)
        return_info = []

        print("SCALEOUT END\n")

        return return_info

    def _scaleout_ws(self, scaleout, scaleoutinfo):
        """."""
        print('SCALEOUT START\n')
        row_info = scaleoutinfo[0]
        col_info = scaleoutinfo[1]
        ene_info = scaleoutinfo[2]

        return_info = []
        print("SCALEOUT END\n")

        return return_info

    def scaleout_OS(self,processor,input_operand,filter_operand,input_buf,filter_buf,stride):
        print('SCALEOUT START','\n')
        info = self.ScaleoutInfo._scaleout_get_info_OS(processor,input_operand,filter_operand)
        result_list = []
        result = [0,0,0,0,0,0,0,0]
        for i in range(info[0]):
            if i != info[0] - 1:
                input_temp = input_operand[i*info[1]:(i+1)*info[1]]
            else:
                input_temp = input_operand33[i*info[1]:]

            for j in range(info[2]):
                print('SCALEUP FOR POD {}X{}'.format(i+1,j+1))
                if j != info[2] - 1:
                    filter_temp = filter_operand[:,j*info[3]:(j+1)*info[3]]
                else:
                    filter_temp = filter_operand[:,j*info[3]:]

                return_info = self.ScaleupBWIdeal.scaleup_bw_ideal(processor,input_temp,filter_temp,input_buf,filter_buf,"OS",stride)
                result_list.append(return_info)

                print('SCALEUP FOR POD {}X{} finished'.format(i+1,j+1),'\n')

        for components in result_list:
            for i in range(len(components[:-1])):
                result[i] = result[i] + components[i]
            result[-1] = max(result[-1],components[-1])

        return result
