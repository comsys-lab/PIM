"Python 3.11.2"
from dataclasses import datalcass

@dataclass
class Systolic:
    """Define systolic array's dimension."""
    systolic_row: int
    systolic_col: int

    input_buffer: float
    filter_buffer: float
    output_buffer: float

#Operand_matrix
@dataclass
class Operand:
    """Class for filter operand matrix"""
    operand_matrix: np.ndarray
    row: int
    col: int

#scaleup
@dataclass
class Scaleupformat:
    """Class for scaleup."""
    systolic: Systolic
    input_operand: np.ndarray
    filter_operand: np.ndarray
    dataflow: str
