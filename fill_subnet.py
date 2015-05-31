__author__ = 'lrx'

from nodes.layer import *
from nodes.connexion import *
from nodes.math_function.math_function import *
from subnet.subnet import *

"""
Class to choose how to fill a subnet with a given input_datasink and output_datasink
Make it possible to test easily different and new implementations
"""
class FillSubnet:

    @staticmethod
    def MLP2(subnet,input_datasink,output_datasink):
        #Define the datasink
        hidden_datasink = Float1D([200])
        #Define the subnets
        s1 = Subnet()
        s2 = Subnet()
        FillSubnet.subnet_connexion_perceptron(s1,input_datasink,hidden_datasink)
        FillSubnet.subnet_connexion_perceptron(s2,hidden_datasink,output_datasink)
        #Connect the subnets
        subnet.connect_nodes(s1,s2)
        subnet.create_input(s1)
        subnet.create_output(s2)


    @staticmethod
    def subnet_connexion_perceptron(subnet,input_datasink,output_datasink):
        #Creating the node
        connexion = FullConnexion(input_datasink, output_datasink)
        layer = PerceptronLayer(output_datasink, Sigmoid)
        #Connecting the nodes
        subnet.connect_nodes(connexion,layer)
        #Create the input and output
        subnet.create_input(connexion)
        subnet.create_output(layer)

    @staticmethod
    def MLP(subnet,input_datasink,output_datasink):
        #Define the datasink
        hidden_datasink = Float1D([200])
        #Create the pipe nodes
        output_layer = PerceptronLayer(output_datasink, Sigmoid)
        hidden_layer = PerceptronLayer(hidden_datasink, Sigmoid)
        connexion1 = FullConnexion(input_datasink, hidden_datasink)
        connexion2 = FullConnexion(hidden_datasink, output_datasink)
        #Connect the pipe nodes
        subnet.connect_nodes(connexion1,hidden_layer)
        subnet.connect_nodes(hidden_layer,connexion2)
        subnet.connect_nodes(connexion2,output_layer)
        #Create the input and output
        subnet.create_input(connexion1)
        subnet.create_output(output_layer)

    @staticmethod
    def Dropout(subnet,input_datasink,output_datasink,p):
        #Define the datasink
        hidden_datasink = Float1D([200])
        #Create the pipe nodes
        output_layer = PerceptronLayer(output_datasink, Sigmoid)
        hidden_layer = PerceptronLayer(hidden_datasink, Sigmoid)
        connexion1 = FullConnexion(input_datasink, hidden_datasink)
        connexion2 = FullConnexion(hidden_datasink, output_datasink)
        dropout1 = DropoutLayer(input_datasink,p)
        dropout2 = DropoutLayer(hidden_datasink,p)
        #Connect the pipe nodes
        subnet.connect_nodes(dropout1,connexion1)
        subnet.connect_nodes(connexion1,hidden_layer)
        subnet.connect_nodes(hidden_layer,dropout2)
        subnet.connect_nodes(dropout2,connexion2)
        subnet.connect_nodes(connexion2,output_layer)
        #Create the input and output
        subnet.create_input(dropout1)
        subnet.create_output(output_layer)
