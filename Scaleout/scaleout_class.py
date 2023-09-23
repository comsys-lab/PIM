"Python 3.11.5"
from dataclasses import dataclass

from .Scaleup.scaleup_class import Scale_up
from .Scaleup.scaleup_class import Operand

@dataclass
class Scale_out:
    """Dataclass for scaleout."""
    scaleup: Scale_up(0,0)
    operand: Operand(0,0)
    row_dim: int
    row_col: int