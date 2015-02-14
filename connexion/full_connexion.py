__author__ = 'marechaux'

import connexion.connexion
from numpy import *

class FullConnexion(connexion.connexion.Connexion):
    """ Basic connection type: all of the ouputs from the input node are connected to
    all the inputs of the output node.

    Attributes:
      matrix (numpy.darray): a matrix of the weights applied to the outputs from the intput node
    """

    def __init__(self, input_node, output_node):
        super().__init__(input_node, output_node)
        self.matrix = zeros((self.input_size, self.output_size))

    def randomize(self):
        """Sets up a random value for all the connections, i.e., randomizes the weight matrix"""
        self.matrix = 0.01*(random.random_sample((self.input_size, self.output_size)) - 0.005)
        #TODO: make parameters

    def propagation(self):
        """Propagates the input data from the input node to the next node, while """
        self.output.input_data_prop[:] = dot(self.input.output_data_prop, self.matrix)

    def backpropagation(self):
        """Backpropagates the error gradient to the input node"""
        self.input.output_data_backprop[:] = dot(self.matrix, self.output.input_data_backprop)

    def learn(self, alpha):
        """Applies the calculated error to the matrix"""
        self.matrix[:, :] -= alpha * dot(matrix(self.input.output_data_prop).transpose(), matrix(self.output.input_data_backprop))