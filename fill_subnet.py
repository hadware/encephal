__author__ = 'lrx'

from classic_subnet import *

"""
Class to choose how to fill a subnet with a given input_datasink and output_datasink
Make it possible to test easily different and new implementations
"""
class FillSubnet:

    @staticmethod
    def MLP1(input_datasink,output_datasink):
        subnet = Subnet()
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
        return subnet

    @staticmethod
    def MLP2(input_datasink,output_datasink):
        subnet = Subnet()
        #Define the subnets
        s1 = FillSubnet.MLP1(input_datasink,output_datasink)
        #Connect the subnets
        subnet.create_input(s1)
        subnet.create_output(s1)
        return subnet

    @staticmethod
    def MLPSerie1(input_datasink,output_datasink):
        subnet = Subnet()
        #Define the datasink
        hidden_datasink = Float1D([200])
        #Define the subnets
        s1 = ClassicSubnet.FullConnexion_PerceptronLayer(input_datasink,hidden_datasink)
        s2 = ClassicSubnet.FullConnexion_PerceptronLayer(hidden_datasink,output_datasink)
        #Connect the subnets
        subnet.connect_nodes(s1,s2)
        subnet.create_input(s1)
        subnet.create_output(s2)
        return subnet

    def MLPParallele1(input_datasink,output_datasink):
        subnet = Subnet()
        n1 = FullConnexion(input_datasink,output_datasink)
        p1 = PerceptronLayer(output_datasink,Sigmoid)
        p11 =PerceptronLayer(output_datasink,Sigmoid)
        n2 = FullConnexion(input_datasink,output_datasink)
        p2 = PerceptronLayer(output_datasink,Sigmoid)
        p22 =PerceptronLayer(output_datasink,Sigmoid)
        n11 =FullConnexion(output_datasink,output_datasink)
        n22 =FullConnexion(output_datasink,output_datasink)
        subnet.connect_nodes(n1,p11)
        subnet.connect_nodes(n2,p22)
        subnet.connect_nodes(p22,n22)
        subnet.connect_nodes(p11,n11)
        subnet.connect_nodes(n11,p1)
        subnet.connect_nodes(n22,p2)
        subnet.create_input(n1)
        subnet.create_output(p1)
        subnet.connect_output(p2)
        subnet.connect_input(n2)
        return subnet


    @staticmethod
    def MLPParallele2(input_datasink,output_datasink):
        subnet = Subnet()
        #Define the subnets
        s1 = FillSubnet.MLP1(input_datasink,output_datasink)
        s2 = FillSubnet.MLP1(input_datasink,output_datasink)
        #Connect the subnets
        subnet.create_input(s1)
        subnet.connect_input(s2)
        subnet.create_output(s1)
        subnet.connect_output(s2)
        return subnet

    @staticmethod
    def MLPParallele3(input_datasink,output_datasink):
        subnet = Subnet()
        #Define the subnets
        s1 = FillSubnet.MLPSerie1(input_datasink,output_datasink)
        s2 = FillSubnet.MLPSerie1(input_datasink,output_datasink)
        #Connect the subnets
        subnet.create_input(s1)
        subnet.connect_input(s2)
        subnet.create_output(s1)
        subnet.connect_output(s2)
        return subnet

    @staticmethod
    def MLP_para3(input_datasink,output_datasink):
        subnet = Subnet()
        #Define the subnets
        s1 = FillSubnet.MLP1(input_datasink,output_datasink)
        s2 = FillSubnet.MLP1(input_datasink,output_datasink)
        s3 = FillSubnet.MLP1(input_datasink,output_datasink)
        #Connect the subnets
        subnet.create_input(s1)
        subnet.connect_input(s2)
        subnet.connect_input(s3)
        subnet.create_output(s1)
        subnet.connect_output(s2)
        subnet.connect_output(s3)
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

