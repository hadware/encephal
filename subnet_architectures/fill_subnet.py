__author__ = 'lrx'

from subnet_architectures.subnet_classic import *

"""
Class to choose how to fill a subnet with a given input_datasink and output_datasink
Make it possible to test easily different and new implementations
"""
class FillSubnet:

    @staticmethod
    def Convolu(input_datasink,output_datasink):
        subnet = Subnet()
        convo1 = ConvolutionalConnexion(input_datasink,(5,5),ZeroPadding.VALID)
        p1 = PerceptronLayer(Unknown)
        n = FullConnexion(Unknown,output_datasink)
        p2 = PerceptronLayer(output_datasink)

        subnet.create_input(convo1)
        subnet.add_after_node(convo1,p1)
        subnet.add_after_node(p1,n)
        subnet.add_after_node(n,p2)
        subnet.create_output(p2)
        return subnet


    @staticmethod
    def Dropout(input_datasink,output_datasink,p):
        subnet = Subnet()
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
        return subnet

