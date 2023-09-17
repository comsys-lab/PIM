"Python 3.11.5"
from dataclasses import dataclass
import numpy as np

@dataclass
class Operand:
    """Dataclass for operand matrix."""
    operand: np.ndarray
    row: int
    col: int
