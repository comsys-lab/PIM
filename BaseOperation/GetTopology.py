import numpy as np

class GetTopology:
    #return topology layer length
    def return_layer_length(self, path):
        with open(path, 'r') as file:
            return sum(1 for _ in file)

    #read files from topology file
    def read_files(self, path):
        topology = np.loadtxt(path, delimiter=',', usecols=np.arange(1,8), dtype=int)

        length = int(len(topology))

        if length == 1:
            return [topology.tolist()]
        else:
            return topology.tolist()

    #Make MNK and Check, integrated
    def process_topology(self, topology):
        result = []
        for i in topology:
            M = int(np.ceil((i[0] - i[2] + i[6]) / i[6]) * np.ceil((i[1] - i[3] + i[6]) / i[6]))
            N = i[2] * i[3] * i[4]
            K = i[5]
            result.append([M, N, K])
        return result

    def return_topology(self,path):
        topology = self.read_files(path)
        return topology, self.process_topology(topology)