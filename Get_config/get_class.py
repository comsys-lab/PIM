"Python 3.11.5"
from dataclasses import dataclass

#Define dataclass that will be used.
@dataclass
class Systolic:
    """Define systolic array's dimension."""
    row: int
    col: int

    input_buf: float
    filter_buf: float
    output_buf: float

@dataclass
class Others:
    """Dataclass for paramters of NPU except systolic array."""
    pod_row: int
    pod_col: int

    num_systolic: int

    bandwidth: float
    latency: float

    dataflow: str

@dataclass
class Npuothers:
    """Dataclass for npu's other parameters."""
    pod_row: int
    pod_col: int
    num_pods: int

    clock_frequency: float
    bandwidth_per_dimm: float
    num_dimms: int
    dataflow: str

@dataclass
class Others:
    """Dataclass for pim's other parameters."""
    pod_row: int
    pod_col: int
    num_pods: int

    clock_freq: float
    bandwidth: float
    latency: float
    dataflow: str

@dataclass
class Dnnsave:
    """Dataclass for saving dnn and save parameters."""
    topology_path: str
    batch: int

    pim_flag: bool
    storing_path: str

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

