__author__ = 'marechaux'

class Network:

    def __init__(self, subnet):

        #TODO: realize different type of copies
        # self.subnet = subnet.copy()
        self.subnet = subnet

        self.sorted_node = self.subnet.schedule()

        for socket in self.subnet.sockets:
            socket.socket_datasink.init_data()

        #Defining the input and output layer
        self.input_layer = self.subnet.input_node_sockets[0].connected_socket
        self.output_layer = self.subnet.output_node_sockets[0].connected_socket


    def propagation(self,learning = True):
        for node_list in self.sorted_node:
            for node in node_list:
                node.propagation(learning)

    def backpropagation(self):
        """"Using the priority list computed by the verify function, we ask each node and connection to compute
        and backpropagate the error gradient, priority "layer" after priority "layer", all in reverse order."""
        for node_list in reversed(self.sorted_node):
            for node in node_list:
                node.backpropagation()

    def learn(self, alpha):
        """Asks all the elements in the network to "apply" the learning deltas they computed"""
        for node_list in self.sorted_node:
            for node in node_list:
                node.learn(alpha)

    def randomize(self):
        self.subnet.randomize()

    def init_buffer(self):
        for socket in self.subnet.sockets:
            socket.socket_datasink.reinit_data()

    def to_protobuf_messageg(self):
        """Uses the scheduled nodes and sockets to build the protobuf graph sent to CUDA"""
        pass
