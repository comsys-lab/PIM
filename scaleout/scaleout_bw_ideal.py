import sys
sys.path.append('/home/sj/simulation/')

from scaleup.ScaleupBWIdeal import ScaleupBWIdeal
from Base.BaseOperation import BaseOperation
from Base.ScaleoutInfo import ScaleoutInfo

class scaleout_bw_ideal:
    def __init__(self):
        self.ScaleupBWIdeal = ScaleupBWIdeal()
        self.BaseOperation = BaseOperation()
        self.ScaleoutInfo = ScaleoutInfo()

    def scaleout_bw_ideal(self,processor,input_operand,filter_operand,input_buf,filter_buf,dataflow,stride):
        if dataflow == "OS":
            return_info = self.scaleout_OS(processor,input_operand,filter_operand,input_buf,filter_buf,stride)
        elif dataflow == "WS":
            return_info = self.scaleout_WS(processor,input_operand,filter_operand,input_buf,filter_buf,stride)
        elif dataflow == "IS":
            return_info = self.scaleout_IS(processor,input_operand,filter_operand,input_buf,filter_buf,stride)
    
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