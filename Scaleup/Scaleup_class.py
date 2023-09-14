"Python 3.10.8"
from dataclasses import dataclass
import numpy as np

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
    input_operand: Operand
    filter_operand: Operand
    dataflow: str
