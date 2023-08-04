import numpy as np

class GetTopology:
    def __init__(self):
        self.topo = []
        self.MNK = []

    def GetTopology(self, path):
        topo, MNK, len_one = self.read_csv(path)

        #If topology file is entered with Original format, we have to convert it into MNK format.
        #If topology file is entered with MNK format, we have to convert it into Original format.
        if MNK:
            self.MNK = topo
            self.Change_MNK_to_Original(self.MNK, len_one)
        else:
            self.topo = topo
            self.Change_Original_to_MNK(self.topo,len_one)
    
        return self.topo, self.MNK
    
    #read files from topology file
    def read_csv(self, path):
        topology = np.loadtxt(path, delimiter=',', usecols=np.arange(1,8), dtype=int)

        #Check Layer length (topology length)
        length = int(len(topology))
        
        if length == 1:
            topo = [topology.tolist()]
            MNK = len(topo) == 4
            len_one = True
        else:
            topo = topology.tolist()
            MNK = len(topo[0]) == 4
            len_one = False
        
        return topo, MNK, len_one
    
    def Change_Original_to_MNK(self, topo_all, len_one):
        if len_one:
            self.MNK.append(self.Change_Original_to_MNK_One_Layer(topo_all))
        else:
            for topo in topo_all:
                self.MNK.append(self.Change_Original_to_MNK_One_Layer(topo))

    def Change_Original_to_MNK_One_Layer(self, topo):
        #Topology is composed of ['run_name',input_width, input_height, filter_width, filter_height,
        #channel, number_of_fiter, stride]
        M = int(np.ceil((topo[1]-topo[3]+topo[7])/topo[7])*np.ceil((topo[2]-topo[4]+topo[7])/topo[7]))
        N = topo[3] * topo[4] * topo[5]
        K = topo[6]
        MNK = [topo[0],M,N,K]

        return MNK

    def Change_MNK_to_Original(self, MNK_all, len_one):
        if len_one:
            self.topo.append(self.Change_MNK_to_Original_One_Layer(MNK_all))
        else:
            for MNK in MNK_all:
                self.topo.append(self.Change_MNK_to_Original_One_Layer(MNK))

    def Change_MNK_to_Original_One_Layer(self, MNK):
        #MNK is composed of ['run_name',M,N,K]
        topo = [MNK[0],MNK[1],1,1,1,MNK[2],MNK[3],1]

        return topo