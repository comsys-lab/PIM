"Python 3.11.5"
from dataclasses import dataclass
import numpy as np

#scaleup
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
    """Class for operand."""
    input_operand: np.ndarray
    filter_operand: np.ndarray

@dataclass
class Others:
    """Class for others"""
    latency: float
    bandwidth: float
    dataflow: str

@dataclass
class Scale_up:
    """Class for scaleup"""
    systolic: Systolic(0,0,0,0,0)
    others: Others(0,0,0)