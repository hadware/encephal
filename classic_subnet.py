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

    @staticmethod
    def LeNetConvoPart(input_datasink,channel_list):
        """ channel_list = (4,6) pour lenet
        4 entrées donc 4 convoLayer
        Puis 6 canaux mais chaque canaux est connecté aux autres donc 6*4 convo
        on aura une liste [ 4, [4,6] , [6, 10]]...
        ou [1,4]... on a [i,j] les 2 canaux quoi"""



    def Convo(subnet,input_datasink,output_datasink,channel_nb):
        #Create the pipe nodes
        convo_shape = (3,3)
        convo = []
        for i in range(channel_nb):
            convo.append(ConvolutionalConnexion(input_datasink,convo_shape,ZeroPadding.valid))

    @staticmethod
    def ConvoLayer(input_datasink,kernel_shape,zero_padding,activation_function,pooling_function, pooling_shape,stride):
        #Creates the pipe nodes
        convo = ConvolutionalConnexion(input_datasink,kernel_shape,zero_padding)
        middle_datasink = convo.output_datasink
        perceptron = PerceptronLayer(middle_datasink, activation_function)
        pooling = PoolingConnexion(middle_datasink,pooling_function,pooling_shape,stride)
        #Creates the subnet
        subnet = Subnet()
        subnet.create_input(convo)
        subnet.add_right_node(convo,perceptron)
        subnet.add_right_node(perceptron,pooling)
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
