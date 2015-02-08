__author__ = 'marechaux'

from numpy import *


class Node:

    def __init__(self, input_size, output_size):
        self.input_connexion = []
        self.output_connexion = []
        self.input_data_prop = None
        self.output_data_prop = None
        self.input_data_backprop = None
        self.output_data_backprop = None
        self.input_size = input_size
        self.output_size = output_size

    def add_input_connexion(self, connexion):
        self.input_connexion.append(connexion)

    def add_output_connexion(self, connexion):
        self.output_connexion.append(connexion)

    def learn(self, alpha):
        pass
