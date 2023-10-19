"Python 3.11.5"
import numpy as np

class GetTopology:
    """Class for reading topology files (.csv format)."""
    def __init__(self):
        self.topo = []
        self.mnk = []
        self.new_topo = []
        self.mac = 0

    #Input: str / Return: list | list
    def get_topology(self, path):
        """From topology file path, return topology and mnk."""
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

        self.new_topo = self.check_topology(self.topo)

        return self.topo, self.mnk, self.new_topo, self.mac

    #Input: str
    def return_layer_length(self, path):
        """Return layer length."""
        with open(path, 'r', encoding="utf-8") as file:
            return sum(1 for _ in file)

    #Input: str / Return: bool
    def check_mnk(self, path):
        """Check whether format of csv file is mnk or not."""
        file = open(path, 'r', encoding="utf-8")
        length = len(file.readline().split(','))
        if length > 5:
            mnk = False
        else:
            mnk = True

        return mnk

    #Input: int | str / Return: list, bool, bool
    def read_csv(self, length, path):
        """Read csv file and return. Check the length, and MNK format."""
        mnk = self.check_mnk(path)
        if not mnk:
            topology = np.loadtxt(path, delimiter=',', usecols=np.arange(1,8), dtype=int)
        else:
            topology = np.loadtxt(path, delimiter=',', usecols=np.arange(1,4), dtype=int)

        #Check Layer length (topology length)
        if length == 1:
            topo = [topology.tolist()]
            len_one = True
        else:
            topo = topology.tolist()
            len_one = False

        return topo, mnk, len_one

    #Input: list | bool
    def change_original_to_mnk(self, topo_all, len_one):
        """Change original format to MNK format."""
        if len_one:
            self.mnk.append(self.change_original_to_mnk_one_layer(topo_all[0]))
        else:
            for topo in topo_all:
                self.mnk.append(self.change_original_to_mnk_one_layer(topo))

    #Input: list / Return: bool
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

        #for the number of MAC operation
        mac = os_input_row * os_input_col * os_filter_col
        self.mac += mac

        return mnk

    #Input: list | bool / Return: bool
    def change_mnk_to_original(self, mnk_all, len_one):
        """Change MNK format to original format."""
        if len_one:
            self.topo.append(self.change_mnk_to_original_one_layer(mnk_all[0]))
        else:
            for mnk in mnk_all:
                self.topo.append(self.change_mnk_to_original_one_layer(mnk))

    def change_mnk_to_original_one_layer(self, mnk):
        """Change MNK format to original format."""
        #MNK is composed of ['run_name',M,N,K]
        topo = [mnk[0],1,1,1,mnk[1],mnk[2],1]

        #for the number of MAC operation
        mac = mnk[0] * mnk[1] * mnk[2]
        self.mac += mac

        return topo

    def check_topology(self, topology):
        """Remove duplication in layer, and check stride."""
        check_layer = []
        for layer in topology:
            if layer not in check_layer:
                check_layer.append(layer)

        new_topo = []
        for i in range(len(check_layer)):
            new_topo.append([0,[]])

        for layer in topology:
            index = check_layer.index(layer)
            new_topo[index][0] += 1
            if new_topo[index][1] == []:
                new_topo[index][1] = layer

        return new_topo
