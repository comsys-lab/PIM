"Python 3.11.5"
from dataclasses import dataclass

from .Scaleup.scaleup_class import Scaleup
from .Scaleup.scaleup_class import Operand

@dataclass
class Scaleout:
    """Dataclass for scaleout."""
    scaleup: Scaleup(0,0)
    operand: Operand(0,0)
    row_dim: int
    row_col: int