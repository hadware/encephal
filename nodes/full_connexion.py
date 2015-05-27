__author__ = 'marechaux'

from numpy import *

from nodes.node import *


class FullConnexion(PipeNode):
    """ Basic connection type: all of the ouputs from the input node are connected to
    all the inputs of the output node.

    Attributes:
      matrix (numpy.darray): a matrix of the weights applied to the outputs from the intput node
    """

    def __init__(self, input_datasync, output_datasync):
        super().__init__(input_datasync.type, output_datasync.type)
        self.matrix = zeros((self.input_size.total_size, self.output_size.total_size))

    def randomize(self):
        """Sets up a random value for all the connections, i.e., randomizes the weight matrix"""
        self.matrix = 0.01*(random.random_sample((self.input_size.total_size, self.output_size.total_size)) - 0.5)
        #TODO: make parameters

    def propagation(self, input_socket, output_socket):
        """Propagates the input data from the input node to the next node, while """
        output_socket.prop_data[:] += dot(input_socket.prop_data, self.matrix)

    def backpropagation(self, input_socket, output_socket):
        """Backpropagates the error gradient to the input node"""
        input_socket.backprop_data[:] += dot(self.matrix, output_socket.backprop_data)

    def learn(self, alpha, input_socket, output_socket):
        """Applies the calculated error to the matrix"""
        self.matrix[:, :] -= alpha * dot(matrix(input_socket.prop_data).transpose(), matrix(output_socket.backprop_data))