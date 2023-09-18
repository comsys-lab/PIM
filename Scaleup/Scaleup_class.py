"Python 3.11.5"
from dataclasses import dataclass
import numpy as np

@dataclass
class Systolic:
    """Define systolic array's dimension."""
    row: int
    col: int

    input_buffer: float
    filter_buffer: float
    output_buffer: float

#scaleup
@dataclass
class Scaleupformat:
    """Class for scaleup."""
    systolic: Systolic
    input_operand: np.ndarray
    filter_operand: np.ndarray
    dataflow: str
