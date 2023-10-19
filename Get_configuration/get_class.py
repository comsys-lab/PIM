"Python 3.11.5"
from dataclasses import dataclass

#Get_configuration.py
@dataclass
class NPU_others:
    """Class for NPU's other parameters."""
    pod_row: int
    pod_col: int
    num_pods: int
    clk_freq: float
    bandwidth: float
    latency: float
    dataflow: str

@dataclass
class NPU_systolic:
    """Class for NPU's systolic parameters."""
    row: int
    col: int
    throughput: float
    input_buffer: float
    filter_buffer: float
    output_buffer: float

@dataclass
class PIM_others:
    """Class for PIM's other parameters."""
    pod_row: int
    pod_col: int
    num_dimms: int
    chips_per_dimm: int
    clk_freq: float
    bandwidth: float
    latency: float
    dataflow: str

@dataclass
class PIM_sysotlic:
    """Class for PIM's systolic parameters."""
    row: int
    col: int
    input_buffer: float
    filter_buffer: float
    output_buffer: float

@dataclass
class Other_params:
    """Class for other parameters."""
    topo_path: str
    batch: int
    pim_flag: bool
    storing_path: str

#Get_energy.py
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