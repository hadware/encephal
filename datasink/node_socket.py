__author__ = 'lrx'

from datasink.datasink import *
from tests.construction.test_construction_exception import *


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

    def check_unknown_type(self,socket):
        if (self.datasink).isUnknown and (socket.socket_datasink).isUnknown:
            raise UnknownNodesCanNotConnectTogether
        elif self.datasink.isUnknown:
            self.node.update_datasink(socket.socket_datasink)
        elif (socket.socket_datasink).isUnknown:
            print('socket de type unknown, à voir si ca arrive')
            socket.socket_datasink = type(self.datasink)(self.datasink.shape_data)
        else:
            return None



class InputNodeSocket(NodeSocket):

    def connect_socket(self, socket):
        self.check_unknown_type(socket)
        if socket.socket_datasink.type.matches(self.datasink.type):
            self.connected_socket = socket
            socket.add_output_node_socket(self)
        else:
            raise WrongSocketDataType()


class OutputNodeSocket(NodeSocket):

    def connect_socket(self, socket):
        self.check_unknown_type(socket)
        if socket.socket_datasink.type.matches(self.datasink.type):
            self.connected_socket = socket
            socket.add_input_node_socket(self)
        else:
            raise WrongSocketDataType()


class WrongSocketDataType(DataTypeError):
    pass