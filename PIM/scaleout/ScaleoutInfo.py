"Python 3.11.5"
import numpy as np

class ScaleoutInfo:
    """For scaleout function."""
    def scaleout_get_info(self, processor, input_operand, filter_operand, dataflow):
        if dataflow == "OS":
            return self._scaleout_get_info_OS(processor, input_operand, filter_operand)
        elif dataflow == "WS":
            return self._scaleout_get_info_WS(processor, input_operand, filter_operand)
        elif dataflow == "IS":
            return self._scaleout_get_info_IS(processor, input_operand, filter_operand)

    def df_os(self):
        pass
    def df_ws(self):
        pass
    def df_is(self):
        pass

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