__author__ = 'lrx'

from classic_subnet import *

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
        s1 = ClassicSubnet.FullConnexion_PerceptronLayer(input_datasink,hidden_datasink)
        s2 = ClassicSubnet.FullConnexion_PerceptronLayer(hidden_datasink,output_datasink)
        #Connect the subnets
        subnet.connect_nodes(s1,s2)
        subnet.create_input(s1)
        subnet.create_output(s2)

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

