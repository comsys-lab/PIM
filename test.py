from Make_Operand.make_operand import MakeOperand
from scaleout.Scaleup.scaleup_dram import Scaleupdram
from scaleout.Scaleup.scaleup_class import Scaleup
from scaleout.Scaleup.scaleup_class import Systolic
from scaleout.Scaleup.scaleup_class import Others
from scaleout.Scaleup.scaleup_class import Operand
from scaleout.Scaleup.scaleup import ScaleUp
import time
syst = Systolic(16,16,4096,4096,4096)
others = Others(0,0,"OS")
scaleup = Scaleup(syst,others)
#topo_one = [512,1,1,1,49154,12288,1]
topo_one = [64,1,1,1,64,768,1]
a = MakeOperand()
inp,fil= a.return_operand_matrix(topo_one, "OS")

Op = Operand(0,0)
Op.input_operand = inp
Op.filter_operand = fil

info = ScaleUp().scaleup_info(scaleup, Op)
runtime = ScaleUp().scaleupruntime.get_runtime(scaleup, Op)

b = Scaleupdram()
start = time.time()
b.df_os(scaleup, Op, info)
end = time.time()
print(end-start)