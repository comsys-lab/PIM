"Python 3.11.5"
import numpy as np

from .Scaleup.scaleup import Scale_up
from .scaleout_class import Scaleout

class Scaleout:
    """."""
    def __init__(self) -> None:
        self.scaleup = Scale_up()

    def scaleout(self):
        pass

    def info(self, scaleout, operand):
        dataflow = scaleout.scaleup.others.dataflow
        if dataflow == "OS":
            row, col = operand.input_operand.row, operand.filter_operand.col
        elif dataflow == "WS":
            row, col = operand.input_operand.row, operand.filter_operand.col
        elif dataflow == "IS":
            row, col = operand.filter_operand.row, operand.input_operand.col

        return row, col

    def scaleout_info(self, scaleout, operand):
        row_dim, col_dim = scaleout.row_dim, scaleout.col_dim
        row, col = self.info(scaleout, operand)
        row_count = min(row, row_dim)
        col_count = min(col, col_dim)
        per_row = int(np.ceil(row / row_count))
        per_col = int(np.ceil(col / col_count))

        row_E_eff = row / row_dim if row <= row_dim else 1
        col_E_eff = col / col_dim if col <= col_dim else 1


        return row_count, per_row, col_count, per_col, row_E_eff, col_E_eff