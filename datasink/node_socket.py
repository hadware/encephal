__author__ = 'lrx'

from datasink.datasink import *


class NodeSocket:
    """
    Represent a nodeSocket on which sockets will connect.
    Helpful for datatype check. Handle all the connexion process
    Attributes:
    node (Node): the node connected to the node socket
    connected_socket (Socket): the socket to which the node is connected through this NodeSocket
    datasink (Datasink): the datasink of the connexion
    IMPORTANT: This datasink has no data neither prop_data nor backprop_data initialized
    """
    def __init__(self, node, datasink):
        self.node = node
        self.connected_socket = None
        self.datasink = datasink

    #Checks if the datatype going out of the node matches the datatype
    def connect_socket(self, socket):
        pass

class InputNodeSocket(NodeSocket):

    def connect_socket(self, socket):
        if socket.socket_datasink.type.matches(self.datasink.type):
            self.connected_socket = socket
            socket.add_output_node_socket(self)
        else:
            raise WrongSocketDataType()


class OutputNodeSocket(NodeSocket):

    def connect_socket(self, socket):
        if socket.socket_datasink.type.matches(self.datasink.type):
            self.connected_socket = socket
            socket.add_input_node_socket(self)
        else:
            raise WrongSocketDataType()


class WrongSocketDataType(DataTypeError):
    pass