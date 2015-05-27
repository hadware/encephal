__author__ = 'marechaux'


from .datasink import *

class WrongSocketDataType(DataTypeError):
    pass

class NodeSocket:
    """A node socket on which sockets will connect, helpful for datatype checks"""
    def __init__(self, node, datatype):
        self.node=node
        self.connected_socket = None
        self.type = datatype #socket the nodesocket will connect to

    def connect_socket(self, socket):
        """Checks if the datatype going out of the node matches the datatype
        of the socket it will go to"""
        pass

class InputNodeSocket(NodeSocket):

    def connect_socket(self, socket):
        if socket.type.matches(self.type):
            self.connected_socket = socket
            socket.add_output_node(self)
        else:
            raise WrongSocketDataType()


class OutputNodeSocket(NodeSocket):

    def connect_socket(self, socket):
        if socket.type.matches(self.type):
            self.connected_socket = socket
            socket.add_input_node(self)
        else:
            raise WrongSocketDataType()


class Node:
    """
    Represents a group of neurons. Usually is connected to one connection on the input,
    and as many as desired on the output.

    Attributes:
      input_connexions (list): list of connexions from which the Node will receive a data array
      output_connexions (list): list of connexions to which the Node will output the data array it processed
      input_data_prop (numpy.ndarray): matrix representing the data the node *receives* before processing it
      output_data_prop (numpy.ndarray): matrix representing the data the node has processed
      input_data_backprop (numpy.ndarray): matrix of the error gradient the node receives
      output_data_backprop (numpy.ndarray): matrix of the error gradient the node computed
      input_size (int): size of the input vector the node receives
      output_size (int): size of the  vector the node outputs
    """

    def __init__(self):
        self.input_node_sockets = []
        self.output_node_sockets = []

    def randomize(self):
        pass

    def learn(self, alpha, input_socket, output_socket):
        """
        Once the error has been computed for a node, this functions tells the node to change its internal values
        using the computed deltas.

        :param alpha: the learning coefficient
        :param input_socket: the input socket, from the feedforward PoV
        :param input_socket: the output socket, from the feedforward PoV
        """
        pass

    def propagation(self, input_socket, output_socket):
        pass

    def backpropagation(self, input_socket, output_socket):
        pass


class PipeNode(Node):
    """A simpler node, with only one input socket, and one output socket, it's
    a parent to most of the conventional NN nodes"""


    def __init__(self, input_datasink, output_datasink):

        self.input_node_sockets = [InputNodeSocket(self,input_datasink.type)]
        self.output_node_sockets = [OutputNodeSocket(self,output_datasink.type)]

        self.output_socket = self.output_node_sockets[0].connected_socket
        self.input_socket = self.input_node_sockets[0].connected_socket

        self.input_shape = input_datasink.shape_data
        self.output_shape = output_datasink.shape_data
        self.input_total_size = input_datasink.total_size()
        self.output_total_size = output_datasink.total_size()

    def connect_to_input(self, socket):
        self.input_node_sockets[0].connect_socket(socket)


    def connect_to_output(self, socket):
        self.output_node_sockets[0].connect_socket(socket)

    @property
    def output_socket(self):
        """Shortcut reference to the output socket"""
        return self.output_node_sockets[0].connected_socket

    @property
    def input_socket(self):
        """Shortcut reference to the input socket"""
        return self.input_node_sockets[0].connected_socket