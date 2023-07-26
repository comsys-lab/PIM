import argparse
from simulation import simulation as sim
import time

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-npu',nargs='*', required=True, help='Enter NPU parameters')
    parser.add_argument('-pim',nargs='*', required=True, help='Enter PIM parameters')
    parser.add_argument('-dnn',nargs='*', required=True, help='Enter DNN parameters')
    parser.add_argument('-save',nargs='*', required=True, help='Enter Save parameters')

    args = parser.parse_args()
    
    npu_param = args.npu
    pim_param = args.pim
    dnn_param = args.dnn
    save_param = args.save

    s = sim()
    start = time.time()
    s.simulation(npu_param,pim_param,dnn_param,save_param)
    end = time.time()


    print(end-start)