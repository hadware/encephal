from scipy.special._ufuncs import nbdtr

__author__ = 'lrx'

from nodes.layer import *
from nodes.connexion import *
from nodes.math_function.math_function import *
from subnet.subnet import *
from subnet_architectures.subnet_architecture import *

    #TODO implement clear exemple AND to prepare some classique structure
    #Convo layer with a length, number of channels and type of pooling


class SubnetClassic:

    """
    Class that creates classic subnet structure
    """

    #TODO: ajouter des stride_shape_list, des kernel_shape_list pour pouvoir parametrer la facon dont sont réalisées
    #TODO: etape par etape les operations


    @staticmethod
    def LeNet(input_datasink,output_datasink):
        subnet = Subnet ()
        nb_channel_list = (4,6)

        list_datasink = [Unknown,Float1D([200]),output_datasink]
        s2 = SubnetClassic.MLP(list_datasink,nb_channel_list[nb_channel_list.__len__()-1])


    @staticmethod
    def MLP(list_datasink):
        subnet = Subnet()
        nb_level = list_datasink.__len__() -1
        list_perceptron_fullconnexion = []
        for i in range(nb_level):
            list_perceptron_fullconnexion.append(SubnetClassic.FullConnexion_PerceptronLayer_generator(list_datasink[i],list_datasink[i+1]))

        subnet.create_input(list_perceptron_fullconnexion[0])
        for i in range(nb_level -1):
            subnet.add_after_node(list_perceptron_fullconnexion[i],list_perceptron_fullconnexion[i+1])
        subnet.create_output(list_perceptron_fullconnexion[nb_level-1])
        return subnet

    @staticmethod
    def LeNetConvoPart(input_datasink,nb_channel_list,kernel_shape_list,stride_shape):
        subnet = Subnet()
        nb_level = nb_channel_list.__len__()
        #Convo
        list_convo_matrix = []
        list_convo_matrix.append(SubnetArchitecture.Matrix(1,nb_channel_list[0],SubnetClassic.Convolution_generator,input_datasink))
        for i in range(nb_level-1):
            list_convo_matrix.append(
                SubnetArchitecture.Matrix(nb_channel_list[i],nb_channel_list[i+1],
                                          SubnetClassic.Convolution_generator,kernel_shape_list[i]))
        #Perceptron and Pooling
        list_perceptron_vector, list_pooling_vector = [], []
        for i in range(nb_level):
            list_perceptron_vector.append(SubnetArchitecture.Vector(nb_channel_list[i],SubnetClassic.Perceptron_generator))
            list_pooling_vector.append(SubnetArchitecture.Vector(nb_channel_list[i],SubnetClassic.Pooling_generator))

        #Connexions
        subnet.create_input(list_convo_matrix[0])
        subnet.add_after_node(list_convo_matrix[0],list_perceptron_vector[0])
        subnet.add_after_node(list_perceptron_vector[0],list_pooling_vector[0])
        for i in range(1,nb_level-1):
            subnet.add_after_node(list_pooling_vector[i-1],list_convo_matrix[i])
            subnet.add_after_node(list_convo_matrix[i],list_perceptron_vector[i])
            subnet.add_after_node(list_perceptron_vector[i],list_pooling_vector[i])
        subnet.add_after_node(list_pooling_vector[nb_level-2],list_convo_matrix[nb_level-1])
        subnet.add_after_node(list_convo_matrix[nb_level-1],list_perceptron_vector[nb_level-1])
        subnet.add_after_node(list_perceptron_vector[nb_level-1],list_pooling_vector[nb_level-1])
        subnet.create_output(list_pooling_vector[nb_level-1])
        return subnet

    @staticmethod
    def Convolution_generator(*args):
        subnet = Subnet()
        convo = ConvolutionalConnexion(args)
        subnet.create_input(convo)
        subnet.create_output(convo)
        return subnet

    @staticmethod
    def Perceptron_generator(*args):
        subnet = Subnet()
        p = PerceptronLayer(args)
        subnet.create_input(p)
        subnet.create_output(p)
        return subnet

    @staticmethod
    def Pooling_generator(*args):
        subnet = Subnet()
        pool = PoolingConnexion(args)
        subnet.create_input(pool)
        subnet.create_output(pool)
        return subnet


    @staticmethod
    def FullConnexion_PerceptronLayer_generator(*args):
        subnet = Subnet()
        fullconnexion = FullConnexion(args[0],args[1])
        p = PerceptronLayer()
        subnet.add_after_node(fullconnexion,p)
        subnet.create_input(fullconnexion)
        subnet.create_output(p)
        return subnet
