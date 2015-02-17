__author__ = 'marechaux'



import connexion.connexion
from numpy import *

class ReferenceReversedConnexion(connexion.connexion.Connexion):

    def __init__(self, input_node, output_node, src_connexion):
        super().__init__(input_node, output_node)
        self.matrix = src_connexion.matrix
        self.delta = src_connexion.delta

    def randomize(self):
        pass
        #self.matrix = random.random_sample((self.input_size, self.output_size))
        #self.matrix = 0.01*(random.random_sample((self.input_size, self.output_size)) - 0.005)
        #TODO: make parameters

    def propagation(self):
        self.output.input_data_prop[:] = dot(self.matrix, self.input.output_data_prop)

    def backpropagation(self):
        self.input.output_data_backprop[:] = dot(self.output.input_data_backprop, self.matrix)

    def learn(self, alpha):
        #self.delta[:, :] = 0.5*self.delta[:, :] - alpha * dot(matrix(self.input.output_data_prop).transpose(), matrix(self.output.input_data_backprop))
        #self.matrix[:, :] += self.delta
        self.matrix[:, :] -= alpha * dot(matrix(self.output.input_data_backprop), matrix(self.input.output_data_prop).transpose())