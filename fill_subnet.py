__author__ = 'lrx'

from subnet.socket_size import *
from nodes.layer import *
from nodes.full_connexion import *
from nodes.math_function.math_function import *

"""
Class to choose how to fill a subnet with a given input_size and output size
Make it possible to test easily different and new implementations
"""

class FillSubnet:

    @staticmethod
    def MLP(subnet,input_size,output_size):

        hidden_size = SocketSize([200])

        output_layer = PerceptronLayer(output_size, Sigmoid)
        output_layer.randomize()

        hidden_layer = PerceptronLayer(hidden_size, Sigmoid)
        hidden_layer.randomize()

        connexion1 = FullConnexion(input_size, hidden_size)
        connexion1.randomize()

        connexion2 = FullConnexion(hidden_size, output_size)
        connexion2.randomize()

        i = subnet.add_input(input_size)
        o = subnet.add_output(output_layer)
        h = subnet.add_node(hidden_layer)
        subnet.add_node(connexion1, i, h)
        subnet.add_node(connexion2, h, o)