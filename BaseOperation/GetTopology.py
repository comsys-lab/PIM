import numpy as np

class GetTopology:
    def __init__(self):
        self.topo = []
        self.MNK = []

    def GetTopology(self, path):
        length = self.return_layer_length(path)
        topo, MNK, len_one = self.read_csv(length, path)

        #If topology file is entered with Original format, we have to convert it into MNK format.
        #If topology file is entered with MNK format, we have to convert it into Original format.
        if MNK:
            self.MNK = topo
            self.Change_MNK_to_Original(self.MNK, len_one)
        else:
            self.topo = topo
            self.Change_Original_to_MNK(self.topo,len_one)

        return self.topo, self.MNK

    def return_layer_length(self, path):
        with open(path, 'r') as file:
            return sum(1 for _ in file)

    #read files from topology file
    def read_csv(self, length, path):
        try:
            topology = np.loadtxt(path, delimiter=',', usecols=np.arange(1,8), dtype=int)
        except:
            topology = np.loadtxt(path, delimiter=',', usecols=np.arange(1,4), dtype=int)
        #Check Layer length (topology length)

        if length == 1:
            topo = [topology.tolist()]
            MNK = len(topo[0]) == 3
            len_one = True
        else:
            topo = topology.tolist()
            MNK = len(topo[0]) == 3
            len_one = False
        print(topo,MNK,len_one)
        return topo, MNK, len_one
    
    def Change_Original_to_MNK(self, topo_all, len_one):
        if len_one:
            self.MNK.append(self.Change_Original_to_MNK_One_Layer(topo_all[0]))
        else:
            for topo in topo_all:
                self.MNK.append(self.Change_Original_to_MNK_One_Layer(topo))

    def Change_Original_to_MNK_One_Layer(self, topo):
        #Topology is composed of [input_width, input_height, filter_width, filter_height,
        #channel, number_of_fiter, stride]
        M = int(np.ceil((topo[0]-topo[2]+topo[6])/topo[6])*np.ceil((topo[1]-topo[3]+topo[6])/topo[6]))
        N = topo[2] * topo[3] * topo[4]
        K = topo[5]
        MNK = [M,N,K]

        return MNK

    def Change_MNK_to_Original(self, MNK_all, len_one):
        if len_one:
            self.topo.append(self.Change_MNK_to_Original_One_Layer(MNK_all[0]))
        else:
            for MNK in MNK_all:
                self.topo.append(self.Change_MNK_to_Original_One_Layer(MNK))

    def Change_MNK_to_Original_One_Layer(self, MNK):
        #MNK is composed of ['run_name',M,N,K]
        print(MNK)
        topo = [MNK[0],1,1,1,MNK[1],MNK[2],1]

        return topo