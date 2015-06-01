__author__ = 'marechaux'

from datasink.node_socket import *

class Node:
    """
    Represents a group of neurons. Usually is connected to one connection on the input,
    and as many as desired on the output.

    Attributes:
      input_node_sockets (list): list of InputNodeSockets reprensenting the "input" plugs from this node
      output_node_sockets (list): list of OutputNodeSockets reprensenting the "output" plugs from this node
    """

    def __init__(self):
        self.input_node_sockets = []
        self.output_node_sockets = []

    def randomize(self):
        pass

    def learn(self, alpha):
        """
        Once the error has been computed for a node, this functions tells the node to change its internal values
        using the computed deltas.

        :param alpha: the learning coefficient
        :param input_socket: the input socket, from the feedforward PoV
        :param input_socket: the output socket, from the feedforward PoV
        """
        pass

    def propagation(self, learning):
        pass

    def backpropagation(self):
        pass


class PipeNode(Node):
    """A simpler node, with only one input socket, and one output socket, it's
    a parent to most of the conventional NN nodes"""
    def __init__(self, input_datasink, output_datasink):
        super().__init__()
        self.input_node_sockets.append(InputNodeSocket(self,input_datasink))
        self.output_node_sockets.append(OutputNodeSocket(self,output_datasink))

    def to_protobuf_message(self, protobuf_message, index):
        """Fills a PipeNode message with the data from the pipenode"""
        protobuf_message.index = index
        self.input_node_socket.datasink.to_protobuff_message(protobuf_message.input_datatype)
        self.output_node_socket.datasink.to_protobuff_message(protobuf_message.output_datatype)
        self._set_protobuff_pipenode_data(protobuf_message)

    def _set_protobuff_pipenode_data(self, pipenode_protobuf_message):
        """Node-specific definition of the pipenodedata"""
        pass

    @property
    def input_shape(self):
        return self.input_node_sockets[0].datasink.shape_data

    @property
    def output_shape(self):
        return self.output_node_sockets[0].datasink.shape_data

    @property
    def input_total_size(self):
        return self.input_node_sockets[0].datasink.total_size

    @property
    def output_total_size(self):
        return self.output_node_sockets[0].datasink.total_size

    @property
    def input_socket(self):
        return self.input_node_sockets[0].connected_socket

    @property
    def output_socket(self):
        return self.output_node_sockets[0].connected_socket

    @property
    def input_node_socket(self):
        return self.input_node_sockets[0]

    @property
    def output_node_socket(self):
        return self.output_node_sockets[0]