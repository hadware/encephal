__author__ = 'marechaux'

from node import *
from numpy import *

class InputLayer(Node):

    def __init__(self, size):
        super().__init__(size, size)
        vector = zeros(size)
        self.input_data_prop = vector
        self.output_data_prop = vector
        self.input_data_backprop = vector
        self.output_data_backprop = vector

    def propagation(self):
        pass


class PerceptronLayer(Node):

    def __init__(self, size, activation_function):
        super().__init__(size, size)
        self.input_data_prop = zeros(size)
        self.output_data_prop = zeros(size)
        self.input_data_backprop = zeros(size)
        self.output_data_backprop = zeros(size)
        self.activation_function = activation_function
        #self.bias = zeros(size)

    def propagation(self):
        self.output_data_prop[:] = self.activation_function.function(self.input_data_prop)

    def backpropagation(self):
        self.input_data_backprop[:] = self.activation_function.differential(self.output_data_prop) * self.output_data_backprop #TODO change differential name...


class OutputLayer(PerceptronLayer):

    def __init__(self, size, activation_function, error_function):
        super().__init__(size, activation_function)
        self.error_function = error_function

    def error(self, expected):
        self.output_data_backprop[:] = self.error_function.differential(self.output_data_prop, expected)
