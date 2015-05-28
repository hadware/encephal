__author__ = 'marechaux'

from numpy import *
from nodes.node import *


class PerceptronLayer(PipeNode):
    """
    A node representing a hidden layer of a perceptron network.

    Attributes:
      bias (numpy.ndarray): a ndarray of the layer's bias value for each unit (neuron)
      activation_function : the function the layer will use on the sum to compute the output value. Usually a sigmoid.
    """

    def __init__(self, datasink, activation_function):
        super().__init__(datasink, datasink)
        self.bias = zeros(self.input_shape)
        self.activation_function = activation_function

    def propagation(self, input_socket, output_socket):
        output_socket.prop_data[:] += self.activation_function.function(input_socket.prop_data + self.bias)

    def backpropagation(self, input_socket, output_socket):
        """Computes the propagated error gradient for the hidden perceptron layer"""
        input_socket.backprop_data[:] += self.activation_function.differential_auxiliary(output_socket.prop_data) * output_socket.backprop_data

    def learn(self, alpha, input_socket, output_socket):
        """Modifies the bias array using the computed (and propagated) error gradient"""
        self.bias[:] -= alpha * input_socket.backprop_data

    def randomize(self):
        """Initialiazises all the biases for each internal neuron to a random value"""
        self.bias[:] = 0.01*(random.random_sample(self.input_shape)-0.5)

class DropoutLayer(PipeNode):
    """
    A node representing a hidden layer of a Droupout.

    Attributes:
      filter (numpy.ndarray): a ndarray of
      p: the probability to keep
    """
    def __init__(self, datasink, p):
        super().__init__(datasink, datasink)
        self.filter = ones(self.input_shape)
        self.p = p

    def propagation(self, learning = True):
        if learning:
            self.filter[:] = random.binomial(1, self.p, self.input_shape)
            self.output_socket.prop_data[:] = self.input_socket.prop_data * self.filter
        else:
            self.output_socket.prop_data[:] = self.input_socket.prop_data

    def backpropagation(self):
        self.input_socket.backprop_data[:] = self.output_socket.backprop_data * self.filter

    def learn(self, alpha):
        pass
