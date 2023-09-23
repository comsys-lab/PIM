"Python 3.11.5"
from Scaleup.scaleup import Scaleup
from Scaleup.base_operation import Baseoperation

from scaleout_class import Scaleout

from scaleup.ScaleupBWIdeal import ScaleupBWIdeal
from Base.BaseOperation import BaseOperation
from Base.ScaleoutInfo import ScaleoutInfo

class Scaleout:
    """Scaleout simulation."""
    def __init__(self):

        self.scaleup = Scaleup()
        self.baseoperation = Baseoperation()

    def _scaleout(self, scaleout, operand):
        """With scaleup(format), operand and stride get information from scaleup"""
        dataflow = scaleout.scaleup.others.dataflow
        if dataflow == "OS":
            pass
        elif dataflow == "WS":
            pass
        elif dataflow == "IS":
            pass

        return 1
    def scaleout(self,processor,input_operand,filter_operand,input_buf,filter_buf,dataflow,stride):
        """With scaleup(format), operand and stride get information from scaleup"""
        if dataflow == "OS":
            return_info = self.scaleout_OS(processor,input_operand,filter_operand,input_buf,filter_buf,stride)
        elif dataflow == "WS":
            return_info = self.scaleout_WS(processor,input_operand,filter_operand,input_buf,filter_buf,stride)
        elif dataflow == "IS":
            return_info = self.scaleout_IS(processor,input_operand,filter_operand,input_buf,filter_buf,stride)

        return return_info
    def df_os(self, scaleout, operand, info, stride):
        """When dataflow is os."""
        for i in range(in)
    def scaleout_OS(self,processor,input_operand,filter_operand,input_buf,filter_buf,stride):
        print('SCALEOUT START','\n')
        info = self.ScaleoutInfo._scaleout_get_info_OS(processor,input_operand,filter_operand)
        result_list = []
        result = [0,0,0,0,0,0,0,0]
        for i in range(info[0]):
            if i != info[0] - 1:
                input_temp = input_operand[i*info[1]:(i+1)*info[1]]
            else:
                input_temp = input_operand[i*info[1]:]

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

    def scaleout_WS(self,processor,input_operand,filter_operand,input_buf,filter_buf,stride):
        print('SCALEOUT START','\n')
        info = self.ScaleoutInfo._scaleout_get_info_WS(processor,input_operand,filter_operand)
        result_list = []
        result = [0,0,0,0,0,0,0,0]
        for i in range(info[0]):
            if i != info[0] - 1:
                input_temp = input_operand[:,i*info[1]:(i+1)*info[1]]
            else:
                input_temp = input_operand[:,i*info[1]:]

            for j in range(info[2]):
                print('SCALEUP FOR POD {}X{}'.format(i+1,j+1))
                if j != info[2] - 1:
                    filter_temp = filter_operand[:,j*info[3]:(j+1)*info[3]]
                else:
                    filter_temp = filter_operand[:,j*info[3]:]

                return_info = self.ScaleupBWIdeal.scaleup_bw_ideal(processor,input_temp,filter_temp,input_buf,filter_buf,"WS",stride)
                result_list.append(return_info)

                print('SCALEUP FOR POD {}X{} finished'.format(i+1,j+1),'\n')
        
        for components in result_list:
            for i in range(len(components[:-1])):
                result[i] = result[i] + components[i]
            result[-1] = max(result[-1],components[-1])
 
        return result
    
    def scaleout_os(self, scaleout, operand, stride):
        pass
    def scaleout_ws(self, scaleout, oeprand, stride):
        pass
    def scaleout_is(self, scaleout, operand, stride):
        pass
    """
    def scaleout_IS(self,processor,input_operand,filter_operand,input_buf,filter_buf,check,stride):
        print('SCALEOUT START','\n')
        info = self.ScaleoutInfo._scaleout_get_info_IS(processor,input_operand,filter_operand)
        result_list = []
        result = [0,0,0,0,0,0,0,0,0]
        for i in range(info[0]):
            if i != info[0] - 1:
                filter_temp = filter_operand[:,i*info[1]:(i+1)*info[1]]
            else:
                filter_temp = filter_operand[:,i*info[1]:]

            for j in range(info[2]):
                print('SCALEUP FOR POD {}X{}'.format(i+1,j+1))
                if j != info[2] - 1:
                    input_temp = input_operand[:,j*info[3]:(j+1)*info[3]]
                else:
                    input_temp = input_operand[:,j*info[3]:]
                
                return_info = self.ScaleupBWIdeal.scaleup_bw_ideal(processor,input_temp,filter_temp,input_buf,filter_buf,"IS",check,stride)
                result_list.append(return_info)
                
        for components in result_list:
            for i in range(len(components[:-1])):
                result[i] = result[i] + components[i]
            result[-1] = max(result[-1],components[-1]) 
        
        return result
        """
    def os_info(self, scaleout, operand):
        pass
    def ws_info(self, scaleout, operand):
        pass
    def is_info(self, scaleout, operand):
        pass

    def scaleout_info(self, scaleout, operand, row, col):
        row_dim, col_dim
        row_count = min(row, scaleout.row_dim)
        col_cout = min(col, scaleout.col_dim)
        per_row = int(np.ceil(row / row_count))
        per_col = int(np.ceil(col / col_count))
        #For energy case
        row_E_eff = row / row_dim if row <= row_dim else 1
        #col_E_eff = col / col_dim if 

    def _scaleout_get_info_OS(self, processor, input_operand, filter_operand):
        return self._scaleout_get_info_common(processor, len(input_operand), len(filter_operand[0]))

    def _scaleout_get_info_WS(self, processor, input_operand, filter_operand):
        return self._scaleout_get_info_common(processor, len(input_operand), len(filter_operand[0]))

    def _scaleout_get_info_IS(self, processor, input_operand, filter_operand):
        return self._scaleout_get_info_common(processor, len(filter_operand), len(input_operand[0]))

    def _scaleout_get_info_common(self, processor, row, col):
        row_dim, col_dim = processor[2], processor[3]
        row_count = min(row, row_dim)
        col_count = min(col, col_dim)
        per_row = int(np.ceil(row / row_count))
        per_col = int(np.ceil(col / col_count))
        row_E_eff = row / row_dim if row <= row_dim else 1
        col_E_eff = col / col_dim if col <= col_dim else 1

        return [row_count, per_row, col_count, per_col, row_E_eff * col_E_eff]