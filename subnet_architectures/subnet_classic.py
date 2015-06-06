__author__ = 'lrx'

from nodes.layer import *
from nodes.connexion import *
from nodes.math_function.math_function import *
from subnet.subnet import *

    #TODO implement clear exemple AND to prepare some classique structure
    #Convo layer with a length, number of channels and type of pooling


class ClassicSubnet:

    """
    Class that creates classic subnet structure
    """


    """ Exemple: Pour Lenet5 nb_channel_list = (4,6) et nb_fullconnexion_perceptron = 2"""
    @staticmethod
    def LeNetConvoPart(input_datasink,nb_channel_list,nb_perceptron,kernel_shape_list,stride_shape):
        subnet = Subnet()
        #Initialisation of all the nodes
        nb_level_convo = nb_channel_list.__len__()

    @staticmethod
    def PerceptronLayer_Pooling(middle_datasink,activation_function,pooling_function, pooling_shape,stride):
        #Creates the pipe nodes
        perceptron = PerceptronLayer(middle_datasink, activation_function)
        pooling = PoolingConnexion(middle_datasink,pooling_function,pooling_shape,stride)
        #Creates the subnet
        subnet = Subnet()
        subnet.create_input(perceptron)
        subnet.add_after_node(perceptron,pooling)
        subnet.create_output(pooling)
        return subnet

    @staticmethod
    def FullConnexion_PerceptronLayer(input_datasink,output_datasink):
        subnet = Subnet()
        #Creating the node
        connexion = FullConnexion(input_datasink, output_datasink)
        perceptron = PerceptronLayer(output_datasink, Sigmoid)
        #Connecting the nodes
        subnet.connect_nodes(connexion,perceptron)
        #Create the input and output
        subnet.create_input(connexion)
        subnet.create_output(perceptron)
        return subnet
