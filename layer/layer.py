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
        self.output_data_backprop = zeros(size)

    def propagation(self, learning = True):
        pass


class PerceptronLayer(Node):

    def __init__(self, size, activation_function):
        super().__init__(size, size)
        self.input_data_prop = zeros(size)
        self.output_data_prop = zeros(size)
        self.input_data_backprop = zeros(size)
        self.output_data_backprop = zeros(size)
        self.bias = zeros(size)
        self.delta = zeros(size)
        self.activation_function = activation_function

        #self.bias = zeros(size)

    def propagation(self, learning = True):
        self.output_data_prop[:] = self.activation_function.function(self.input_data_prop + self.bias)

    def backpropagation(self):
        self.input_data_backprop[:] = self.activation_function.differential(self.output_data_prop) * self.output_data_backprop #TODO change differential name...

    def learn(self, alpha):
        #pass
        self.bias[:] -= alpha * self.input_data_backprop

    def randomize(self):
        self.bias[:] = 0.01*(random.random_sample(self.input_size)-0.005)
        #self.bias[:] = (random.random_sample(self.input_size))
        #TODO: make parameters


class OutputLayer(PerceptronLayer):

    def __init__(self, size, activation_function, error_function):
        super().__init__(size, activation_function)
        self.error_function = error_function

    def grad_error(self, expected):
        self.output_data_backprop[:] = self.error_function.differential(self.output_data_prop, expected)
        #print(self.output_data_backprop[:])

    def error(self, expected):
        return sum(self.error_function.function(self.output_data_prop, expected))


class DropoutLayer(Node):

    def __init__(self, size, p):
        super().__init__(size, size)
        self.input_data_prop = zeros(size)
        self.output_data_prop = zeros(size)
        self.input_data_backprop = zeros(size)
        self.output_data_backprop = zeros(size)
        self.filter = ones(size)
        self.p = p

    def propagation(self, learning = True):
        if learning:
            self.filter[:] = random.binomial(1, self.p, self.input_size)
            self.output_data_prop[:] = self.input_data_prop * self.filter
        else:
            self.output_data_prop[:] = self.input_data_prop
        #print(self.output_data_prop)

    def backpropagation(self):
        self.input_data_backprop[:] = self.output_data_backprop * self.filter

    def learn(self, alpha):
        pass