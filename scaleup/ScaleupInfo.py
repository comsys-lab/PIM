import numpy as np

class ScaleupInfo:
    #This function get scaleup information from input and filter matrix.
    #Dimension of operand matrix different depending on the dataflow.

    def ScaleupInfo(self, processor, input_operand, filter_operand, dataflow):
        #Processor is entered in the form of lists: [systolic_row, systolic_col, pod_dimension_row, pod_dimension_col]
        #However, in scaleup case, simulator only needs the dimension of systolic array: [systolic_row, systolic_col]
        Sys_Row, Sys_Col = processor[0], processor[1]
        row, col = self._get_operand_dimensions(input_operand, filter_operand, dataflow)
        num_row_tiles, num_col_tiles = self._get_row_num_col_tile(Sys_Row, Sys_Col, row, col)

        return num_row_tiles, num_col_tiles

    #Dimension of operand matrix is different only with IS dataflow.
    def _get_operand_dimensions(self, input_operand, filter_operand, dataflow):
        if dataflow == "IS":
            return len(filter_operand), len(input_operand[0])
        else:
            return len(input_operand), len(filter_operand[0])

    #Calculate number of tiles
    def _get_num_tiles(self, Sys_Row, Sys_Col, row, col):
        num_row_tiles = int(np.ceil(row / Sys_Row))
        num_col_tiles = int(np.ceil(col / Sys_Col))

        return num_row_tiles, num_col_tiles