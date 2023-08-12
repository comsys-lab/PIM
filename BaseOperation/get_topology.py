"Python 3.10.8"
import numpy as np

class GetTopology:
    """
    There are functions to read topology files (.csv format).
    .
    """
    def __init__(self):
        self.topo = []
        self.mnk = []

    def get_topology(self, path) -> list | list:
        """
        .
        """
        length = self.return_layer_length(path)
        topo, mnk, len_one = self.read_csv(length, path)

        #If topology file is entered with Original format, we have to convert it into MNK format.
        #If topology file is entered with MNK format, we have to convert it into Original format.
        if mnk:
            self.mnk = topo
            self.change_mnk_to_original(self.mnk, len_one)
        else:
            self.topo = topo
            self.change_original_to_mnk(self.topo,len_one)

        return self.topo, self.mnk

    def return_layer_length(self, path):
        """
        .
        """
        with open(path, 'r', encoding="utf-8") as file:
            return sum(1 for _ in file)

    #read files from topology file
    def read_csv(self, length, path):
        """"
        .
        """
        try:
            topology = np.loadtxt(path, delimiter=',', usecols=np.arange(1,8), dtype=int)
        except BaseException:
            topology = np.loadtxt(path, delimiter=',', usecols=np.arange(1,4), dtype=int)

        #Check Layer length (topology length)
        if length == 1:
            topo = [topology.tolist()]
            mnk = len(topo[0]) == 3
            len_one = True
        else:
            topo = topology.tolist()
            mnk = len(topo[0]) == 3
            len_one = False

        return topo, mnk, len_one

    def change_original_to_mnk(self, topo_all, len_one):
        """"
        .
        """
        if len_one:
            self.mnk.append(self.change_original_to_mnk_one_layer(topo_all[0]))
        else:
            for topo in topo_all:
                self.mnk.append(self.change_original_to_mnk_one_layer(topo))

    def change_original_to_mnk_one_layer(self, topo):
        """
        Topology is composed of [Input_W, Input_H, Filter_W, Filter_H, Channel, Num_filter, Stride]
        In this function, base dataflow is OS.
        """

        output_row = int(np.ceil((topo[0]-topo[2]+topo[6])/topo[6]))
        output_col = int(np.ceil((topo[1]-topo[3]+topo[6])/topo[6]))

        os_input_row = output_row * output_col
        os_input_col = topo[2] * topo[3] * topo[4]
        os_filter_col = topo[5]
        mnk = [os_input_row, os_input_col, os_filter_col]

        return mnk

    def change_mnk_to_original(self, mnk_all, len_one):
        """
        .
        """
        if len_one:
            self.topo.append(self.change_mnk_to_original_one_layer(mnk_all[0]))
        else:
            for mnk in mnk_all:
                self.topo.append(self.change_mnk_to_original_one_layer(mnk))

    def change_mnk_to_original_one_layer(self, mnk):
        """
        .
        """
        #MNK is composed of ['run_name',M,N,K]
        topo = [mnk[0],1,1,1,mnk[1],mnk[2],1]

        return topo
