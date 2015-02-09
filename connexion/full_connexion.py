__author__ = 'marechaux'

import connexion.connexion
from numpy import *

class FullConnexion(connexion.connexion.Connexion):

    def __init__(self, input_node, output_node):
        super().__init__(input_node, output_node)
        self.matrix = zeros((self.input_size, self.output_size))
        self.delta = zeros((self.input_size, self.output_size))

    def randomize(self):
        #self.matrix = random.random_sample((self.input_size, self.output_size))
        self.matrix = 0.01*(random.random_sample((self.input_size, self.output_size)) - 0.005)
        #TODO: make parameters

    def propagation(self):
        self.output.input_data_prop[:] = dot(self.input.output_data_prop, self.matrix)

    def backpropagation(self):
        self.input.output_data_backprop[:] = dot(self.matrix, self.output.input_data_backprop)

    def learn(self, alpha):
        #self.delta[:, :] = 0.5*self.delta[:, :] - alpha * dot(matrix(self.input.output_data_prop).transpose(), matrix(self.output.input_data_backprop))
        #self.matrix[:, :] += self.delta
        self.matrix[:, :] -= alpha * dot(matrix(self.input.output_data_prop).transpose(), matrix(self.output.input_data_backprop))