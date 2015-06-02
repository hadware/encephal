__author__ = 'lrx'

from nodes.layer import *
from nodes.connexion import *
from nodes.math_function.math_function import *
from subnet.subnet import *

    #TODO implement clear exemple AND to prepare some classique structure
    #Convo layer with a length, number of channels and type of pooling

"""
Class that create classic subnet structure
"""
class ClassicSubnet:

    """@staticmethod
    def ConvoLayer(subnet,input_datasink):
        #Create the pipe nodes
        ConvolutionalConnexion
        PerceptronLayer(output_datasink, Sigmoid)

        #Create the input and output
        subnet.create_input(dropout1)
        subnet.create_output(output_layer)"""

    @staticmethod
    def FullConnexion_PerceptronLayer(input_datasink,output_datasink):
        subnet = Subnet()
        #Creating the node
        connexion = FullConnexion(input_datasink, output_datasink)
        layer = PerceptronLayer(output_datasink, Sigmoid)
        #Connecting the nodes
        subnet.connect_nodes(connexion,layer)
        #Create the input and output
        subnet.create_input(connexion)
        subnet.create_output(layer)
        return subnet
