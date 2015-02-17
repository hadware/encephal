__author__ = 'marechaux'

import connexion.connexion
from numpy import *

class CopyConnexion(connexion.connexion.Connexion):

    def __init__(self, input_node, output_node):
        super().__init__(input_node, output_node)

    def propagation(self):
        self.output.input_data_prop[:] = self.input.output_data_prop

    def backpropagation(self):
        self.input.output_data_backprop[:] = self.output.input_data_backprop

    def learn(self, alpha):
        pass