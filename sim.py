import argparse
from simulation import simulation as sim
import time

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-t',required=True, help='Enter topology file path')
    parser.add_argument('-c',required=True, help='Enter configuration file path')

    args = parser.parse_args()
    
    topology_path = args.t
    configuration_path = args.c

    s = sim()
    s.simulation(topology_path, configuration_path)