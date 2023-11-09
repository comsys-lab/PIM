from Make_Operand.make_operand import MakeOperand
from Scaleout.Scaleup.scaleup_dram import Scaleupdram
from Scaleout.Scaleup.base_class import Scaleup
from Scaleout.Scaleup.base_class import Systolic
from Scaleout.Scaleup.base_class import Others
from Scaleout.Scaleup.base_class import Operand
from Scaleout.Scaleup.scaleup import ScaleUp
import time
syst = Systolic(16,16,8192,8192,8192)
others = Others(0,0,"WS",1024)
scaleup = Scaleup(syst,others)
topo_one = [66,1,1,1,768,96,1]
#topo_one = [64,1,1,1,64,768,1]
a = MakeOperand()
inp,fil= a.return_operand_matrix(topo_one, "WS")

Op = Operand(0,0)
Op.input_operand = inp
Op.filter_operand = fil

info = ScaleUp().scaleup_info(scaleup, Op)

b = ScaleUp()
b.scale_up(scaleup, Op, 1)
