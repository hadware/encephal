__author__ = 'marechaux'

from sys import maxsize

#TODO: check validity of the graph for complex case

class Network:

    def __init__(self, subnet):

        #self.subnet = subnet.copy()
        self.subnet = subnet
        self.sorted_node = None
        self.schedule()

        for socket in self.subnet.sockets:
            socket.socket_datasink.init_data()

        self.input_layer = self.subnet.input_node_sockets[0].connected_socket
        self.output_layer = self.subnet.output_node_sockets[0].connected_socket

    def schedule(self):
        unscheduled_sockets = list(self.subnet.sockets)

        for socket in unscheduled_sockets:
            socket.level = maxsize

        k = -1
        print("début")
        while unscheduled_sockets:
            k += 1
            for socket in unscheduled_sockets:
                candidate = True
                for node in socket.input_nodes:
                    if node.input_socket.level >= k:
                        candidate = False
                if candidate:
                    socket.level = k
                    unscheduled_sockets.remove(socket)

        self.sorted_node = []

        for i in range(k):
            self.sorted_node.append([])

        for node in self.subnet.nodes:
            self.sorted_node[node.input_socket.level].append(node)

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