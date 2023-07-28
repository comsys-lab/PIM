import math
import numpy as np
from tqdm import tqdm

from simulation.make_operand.MakeOperand import make_operand
from basic.basic_operation import basic_operation
from scaleup import scaleup

class scaleout_ideal:
    def __init__(self):
        self.make_operand = make_operand()
        self.scaleup = scaleup()
        self.BO = basic_operation()

    #for scaleout
    #1. get total input & output operand - done by basic.make_operand
    #2. get tiling information & calculate (scaleup -> scaleout)
    #3. scaleup_ideal per tiled operand matrix
    #-----------------------------------------------------------------------
    def scaleout_get_info(self,processor,input_operand,filter_operand):
        row = len(input_operand)
        col = len(filter_operand[0])

        row_count = math.ceil(row / processor[2])
        col_count = math.ceil(col / processor[3])

        row_tiled = math.ceil(row / row_count)
        col_tiled = math.ceil(col / col_count)

        return [row_count,col_count,row_tiled,col_tiled]

    #-----------------------------------------------------------------------
    def scaleout(self,processor,input_operand,filter_operand):
        info = self.scaleout_get_info(processor,input_operand,filter_operand)

    def scaleout_OS(self,processor,input_operand,filter_operand):
        for i in r
    def scaleout_WS(self,processor,input_operand,filter_operand):
        pass
    def scaleout_IS(self,processor,input_operand,filter_operand):
        pass


