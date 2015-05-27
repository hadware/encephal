__author__ = 'marechaux'


from numpy import *

class Socket:
    """
    Represent a socket which is the main element for element's storage
    Attributs:
        input_node_sockets (list of InputNodeSocket):
        output_node_sockets (list of OutputNodeSocket):
        socket_datasink (datasink):
    """

    def __init__(self, datasink):
        self.input_node_sockets = []
        self.output_node_sockets = []
        self.socket_datasink = type(datasink)(datasink.shape_data)
        print(type(self.socket_datasink))

    @property
    def prop_data(self):
        return self.socket_datasink.prop_data

    @property
    def backprop_data(self):
        return self.socket_datasink.backprop_data

    def add_output_node_socket(self, node):
        self.output_node_sockets.append(node)

    def add_input_node_socket(self, node):
        self.input_node_sockets.append(node)

    @property
    def input_nodes(self):
        l=[]
        for node_socket in self.input_node_sockets:
            l.append(node_socket.node)
        return l