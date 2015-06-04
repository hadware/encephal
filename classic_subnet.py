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
    """@staticmethod
    def LeNetConvoPart(input_datasink,nb_channel_list,nb_perceptron,kernel_shape_list,stride_shape):
        #Initialisation of all the nodes
        nb_level_convo = nb_channel_list.__len__()
        convoconnexion_list = []
        pooling_list = []
        fullconnexion_list = []

        nb_channel_left = 1
        for i in range(nb_level_convo):
            nb_channel_right = nb_channel_list[i]
            convoconnexion_list.append(ClassicSubnet.matrixListConvo(nb_channel_left,nb_channel_right))
            pooling_list.append(ClassicSubnet.VectorListPooling(convoconnexion_list,nb_channel_right))
            nb_channel_left = nb_channel_right

        for i in range(nb_perceptron):
            fullconnexion_list.append(ClassicSubnet.VectorListFullConnexion())

        #Connexion between them
        subnet = Subnet()
        for convo_channel in convoconnexion_list[0]:
            for convo in convo_channel:
                subnet.create_input(convo)

        for num in range(1,nb_level_convo):

    @staticmethod
    def VectorListPooling(self,nb_channel_left,nb_channel_right):
        pass

    @staticmethod
    def matrixListConvo(self,nb_channel_left,nb_channel_right):
        pass"""



    def Convo(subnet,input_datasink,output_datasink,channel_nb):
        #Create the pipe nodes
        convo_shape = (3,3)
        convo = []
        for i in range(channel_nb):
            convo.append(ConvolutionalConnexion(input_datasink,convo_shape,ZeroPadding.valid))

    @staticmethod
    def PerceptronLayer_Pooling(input_datasink,activation_function,pooling_function, pooling_shape,stride):
        #Creates the pipe nodes
        middle_datasink = input_datasink
        perceptron = PerceptronLayer(middle_datasink, activation_function)
        pooling = PoolingConnexion(middle_datasink,pooling_function,pooling_shape,stride)
        #Creates the subnet
        subnet = Subnet()
        subnet.create_input(perceptron)
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
