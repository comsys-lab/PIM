"Python 3.10.8"
import numpy as np

class ScaleupInfo:
    """
    Get scaleup information from input and filter matrix.
    Dimension of operand matrix is different depending on the dataflow.
    """
    def scaleupinfo(self, systolic, input_operand, filter_operand, dataflow):
        """
        Get scaleup information form processor and operand matrix.
        Processor is entered in the form of lists: [sys_row, sys_col, pod_dim_row, pod_dim_col]
        In scaleup case, simulator only needs the dimension of systolic array: [sys_row, syscol]
        """
        sys_row, sys_col = systolic.systolic_row, systolic.systolic_col
        row, col = self._get_operand_dimensions(input_operand, filter_operand, dataflow)
        num_row_tiles, num_col_tiles = self._get_num_tiles(sys_row, sys_col, row, col)

        return num_row_tiles, num_col_tiles

    #Dimension of operand matrix is different only with IS dataflow.
    def _get_operand_dimensions(self, input_operand, filter_operand, dataflow):
        """Get operand dimension."""
        if dataflow == "IS":
            return len(filter_operand), len(input_operand[0])
        else:
            return len(input_operand), len(filter_operand[0])

    #Calculate number of tiles
    def _get_num_tiles(self, sys_row, sys_col, row, col):
        num_row_tiles = int(np.ceil(row / sys_row))
        num_col_tiles = int(np.ceil(col / sys_col))

        return num_row_tiles, num_col_tiles
