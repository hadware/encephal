__author__ = 'marechaux'

from numpy import *


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

    def __init__(self, input_size, output_size):
        self.input_size = input_size
        self.output_size = output_size

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
