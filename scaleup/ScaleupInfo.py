import numpy as np

class ScaleupInfo:
    def scaleup_get_info(self, processor, input_operand, filter_operand, dataflow):
        row, col = self._get_operand_dimensions(input_operand, filter_operand, dataflow)
        row_count, col_count = self._get_row_col_count(row, col, processor)
        return [row_count, col_count]

    def _get_operand_dimensions(self, input_operand, filter_operand, dataflow):
        if dataflow == "IS":
            return len(filter_operand), len(input_operand[0])
        else:
            return len(input_operand), len(filter_operand[0])

    def _get_row_col_count(self, row, col, processor):
        row_count = int(np.ceil(row / processor[0]))
        col_count = int(np.ceil(col / processor[1]))
        return row_count, col_count