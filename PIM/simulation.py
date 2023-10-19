"Python 3.10.8"
import argparse

from simulation_base import Simulation

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-t', required=True, help='Enter topology file path')
    parser.add_argument('-c', required=True, help='Enter configuration file path')
    parser.add_argument('-e', required=True, help='Enter energy file path')
    parser.add_argument('-s', required=True, help='Enter storage file path')

    args = parser.parse_args()

    topology_path = args.t
    configuration_path = args.c
    energy_file_path = args.e
    storage_file_path = args.s

    Simulation = Simulation()
    Simulation.simulation(topology_path, configuration_path, energy_file_path, storage_file_path)
