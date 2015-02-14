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
        self.input_connexions = []
        self.output_connexions = []
        self.input_data_prop = None
        self.output_data_prop = None
        self.input_data_backprop = None
        self.output_data_backprop = None
        self.input_size = input_size
        self.output_size = output_size

    def add_input_connexion(self, connexion):
        """Adds an input connection to the node's connections"""
        self.input_connexions.append(connexion)

    def add_output_connexion(self, connexion):
        """Adds an output conneciton to the node's connections"""
        self.output_connexions.append(connexion)

    def learn(self, alpha):
        """
        Once the error has been computed for a node, this functions tells the node to change its internal values
        using the computed deltas.

        :param alpha: the learning coefficient
        """


        pass
