"Python 3.11.5"
from dataclasses import dataclass
import numpy as np

@dataclass #5 Parameters - consistent paramters
class Systolic:
    """Define systolic array's dimension."""
    row: int
    col: int
    input_buffer: float
    filter_buffer: float
    output_buffer: float

@dataclass #3 Parameters - consistent paramters
class Others:
    """Class for other parameters."""
    latency: float
    bandwidth: float
    dataflow: str
    clk_freq: float

@dataclass #4 Parameters - consistent paramters
class Scaleup:
    """Class for scaleup"""
    systolic: Systolic(0,0,0,0,0)
    others: Others(0,0,0,0)

@dataclass #2 Parameters - variable parameters by layers
class Operand:
    """Class for operand."""
    input_operand: np.ndarray
    filter_operand: np.ndarray

@dataclass #2 Parameters - variable parameters by layers
class Scaleout:
    """Class for scaleout."""
    scaleup: Scaleup(0,0)
    operand: Operand(0,0)
    row_dim: int
    col_dim: int

@dataclass #8 paramters - variable for results
class Results:
    """Class for scaleup results."""
    input_sram: int
    filter_sram: int
    output_sram: int
    input_dram: int
    filter_dram: int
    output_dram: int
    runtime: int
    ene_eff: float
