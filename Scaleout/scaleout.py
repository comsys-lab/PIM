"Python 3.11.5"

from Scaleup.scaleup import Scaleup

class Scaleout:
    """."""
    def __init__(self) -> None:
        self.scaleup = Scaleup()

    def scaleout(self):
        pass
        #something->maybe dimension of pods
    def scaleout_info(self, something):
        row_dim,col_dim = something.row_dim, something.col_dim
        

    def _scaleout_get_info_common(self, processor, row, col):
        row_dim, col_dim = processor[2], processor[3]
        row_count = min(row, row_dim)
        col_count = min(col, col_dim)
        per_row = int(np.ceil(row / row_count))
        per_col = int(np.ceil(col / col_count))
        row_E_eff = row / row_dim if row <= row_dim else 1
        col_E_eff = col / col_dim if col <= col_dim else 1

        return [row_count, per_row, col_count, per_col, row_E_eff * col_E_eff]