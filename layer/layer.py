__author__ = 'marechaux'

from node import *
from numpy import *

class InputLayer(Node):
    """
    Acts as a simple placeholder for the input data, so it's relayed to the other nodes of the network.
    """

    def __init__(self, size):
        super().__init__(size, size)
        vector = zeros(size)
        self.input_data_prop = vector
        self.output_data_prop = vector
        self.input_data_backprop = vector
        self.output_data_backprop = zeros(size)

    def propagation(self):
        pass


class PerceptronLayer(Node):
    """
    A node representing a hidden layer of a perceptron network.

    Attributes:
      bias (numpy.ndarray): a matrix of the layer's bias value for each unit (neuron)
      activation_function : the function the layer will use on the sum to compute the output value. Usually a sigmoid.
    """

    def __init__(self, size, activation_function):
        super().__init__(size, size)
        self.input_data_prop = zeros(size)
        self.output_data_prop = zeros(size)
        self.input_data_backprop = zeros(size)
        self.output_data_backprop = zeros(size)
        self.bias = zeros(size)
        self.activation_function = activation_function

    def propagation(self):
        self.output_data_prop[:] = self.activation_function.function(self.input_data_prop + self.bias)

    def backpropagation(self):
        """Computes the propagated error gradient for the hidden perceptron layer"""
        self.input_data_backprop[:] = self.activation_function.differential(self.output_data_prop) * self.output_data_backprop #TODO change differential name...

    def learn(self, alpha):
        """Modifies the bias array using the computed (and propagated) error gradient"""
        self.bias[:] -= alpha * self.input_data_backprop

    def randomize(self):
        """Initialiazises all the biases for each internal neuron to a random value"""
        self.bias[:] = 0.01*(random.random_sample(self.input_size)-0.005)
        #TODO: make parameters


class OutputLayer(PerceptronLayer):
    """
    Output node of a network.
    """

    def __init__(self, size, activation_function, error_function):
        super().__init__(size, activation_function)
        self.error_function = error_function

    def grad_error(self, expected):
        """Computes the error gradient for the output layer"""
        self.output_data_backprop[:] = self.error_function.differential(self.output_data_prop, expected)

    def error(self, expected):
        return sum(self.error_function.function(self.output_data_prop, expected))
