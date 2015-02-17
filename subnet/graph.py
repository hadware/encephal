__author__ = 'marechaux'


from numpy import *

class Socket:

    def __init__(self, size):
        self.prop_data = None
        self.backprop_data = None
        self.size = size
        self.input_nodes = []
        self.output_nodes = []

    def init_data(self):
        self.prop_data = zeros(self.size)
        self.backprop_data = zeros(self.size)

    def reinit_data(self):
        self.prop_data[:] = zeros(self.size)
        self.backprop_data[:] = zeros(self.size)



class GraphSubnet:

    def __init__(self, subnet, input_sockets, output_sockets):
        self.input_sockets = input_sockets
        self.output_sockets = output_sockets
        self.subnet = subnet


class GraphNode:

    def __init__(self, node, input_socket, output_socket):
        self.node = node
        self.input_socket = input_socket
        self.output_socket = output_socket
        input_socket.output_nodes.append(self)
        output_socket.input_nodes.append(self)