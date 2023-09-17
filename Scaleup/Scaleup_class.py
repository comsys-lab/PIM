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

@dataclass
class Operand:
    """Dataclass for operand matrix."""
    operand: np.ndarray
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
