"Python 3.10.8"
from dataclasses import dataclass
import numpy as np

#Define dataclass that will be used.
#get_configuration
@dataclass
class Systolic:
    """Define systolic array's dimension."""
    systolic_row: int
    systolic_col: int

    input_buffer: float
    filter_buffer: float
    output_buffer: float

@dataclass
class Npuothers:
    """Dataclass for npu's other parameters."""
    pod_dimension_row: int
    pod_dimension_col: int
    number_of_pods: int

    clock_frequency: float
    bandwidth_per_dimm: float
    number_of_dimms: int
    dataflow: str

@dataclass
class Pimothers:
    """Dataclass for pim's other parameters."""
    pod_dimension_row: int
    pod_dimension_col: int
    chips_per_dimm: int
    number_of_dimms: int

    clock_frequency: int
    bandwidth_per_dimm: float
    dataflow: str

@dataclass
class Dnnsave:
    """Dataclass for saving dnn and save parameters."""
    topology_path: str
    batch: int

    pim_flag: bool
    storing_path: str

#get_energy
@dataclass
class MACenergy:
    """MAC parameters"""
    mac_random: float
    mac_reused: float
    mac_gated: float
    mac_idle: float

@dataclass
class Energy:
    """Energy parameters"""
    sram_read: float
    sram_write: float
    dram_read: float
    dram_write: float
    mac_energy: float
    mac_idle: float

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
    num_row_tiles: int
    num_col_tiles: int
    input_operand: np.ndarray
    filter_operand: np.ndarray
    dataflow: str