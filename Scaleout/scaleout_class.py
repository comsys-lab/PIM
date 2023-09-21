"Python 3.11.5"
from dataclasses import dataclass

from Scaleup.scaleup_class import Scaleup
from Scaleup.scaleup_class import Operand

@dataclass
class Scaleout:
    """."""
    scaleup: Scaleup()
    operand: Operand(0,0)