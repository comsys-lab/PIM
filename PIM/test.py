from Make_Operand.make_operand import MakeOperand
from PIM.Scaleout.Scaleup.scaleup_dram_ss import Scaleupdram
from PIM.Scaleout.Scaleup.base_class import Scaleup
from PIM.Scaleout.Scaleup.base_class import Systolic
from PIM.Scaleout.Scaleup.base_class import Others
from PIM.Scaleout.Scaleup.base_class import Operand
from Scaleout.Scaleup.scaleup import ScaleUp
import time
syst = Systolic(16,16,4096,4096,4096)
others = Others(0,0,"OS")
scaleup = Scaleup(syst,others)
topo_one = [64,1,1,1,768,64,1]
#topo_one = [64,1,1,1,64,768,1]
a = MakeOperand()
inp,fil= a.return_operand_matrix(topo_one, "OS")

Op = Operand(0,0)
Op.input_operand = inp
Op.filter_operand = fil

info = ScaleUp().scaleup_info(scaleup, Op)
runtime = ScaleUp().scaleupruntime.get_runtime(scaleup, Op)
print(1)
b = Scaleupdram()
start = time.time()
b.df_os(scaleup, Op, info)
end = time.time()
print(end-start)