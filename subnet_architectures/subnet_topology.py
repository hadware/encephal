__author__ = 'lrx'

from subnet_architectures.subnet_classic import *

"""
Class to choose how to test for different topologies.
Subnet in series, Subnet of Subnet or even Subnet in Parallel
"""
class SubnetTopology:

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
        s1 = SubnetTopology.MLP1(input_datasink,output_datasink)
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
        s1 = SubnetTopology.MLP1(input_datasink,output_datasink)
        s2 = SubnetTopology.MLP1(input_datasink,output_datasink)
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
        s1 = SubnetTopology.MLPSerie1(input_datasink,output_datasink)
        s2 = SubnetTopology.MLPSerie1(input_datasink,output_datasink)
        #Connect the subnets
        subnet.create_input(s1)
        subnet.connect_input(s2)
        subnet.create_output(s1)
        subnet.connect_output(s2)
        return subnet

    @staticmethod
    def MLPParallele4(input_datasink,output_datasink):
        subnet = Subnet()
        #Define the subnets
        s1 = SubnetTopology.MLP1(input_datasink,output_datasink)
        s2 = SubnetTopology.MLP1(input_datasink,output_datasink)
        s3 = SubnetTopology.MLP1(input_datasink,output_datasink)
        #Connect the subnets
        subnet.create_input(s1)
        subnet.connect_input(s2)
        subnet.connect_input(s3)
        subnet.create_output(s1)
        subnet.connect_output(s2)
        subnet.connect_output(s3)
        return subnet

    def MLPParalleleParallele1(input_datasink,output_datasink):
        subnet = Subnet()
        #Create the subnet
        s1 = SubnetTopology.MLPParallele2(input_datasink,output_datasink)
        s2 = SubnetTopology.MLPParallele2(input_datasink,output_datasink)
        #Connect the subnets
        subnet.create_input(s1)
        subnet.connect_input(s2)
        subnet.create_output(s1)
        subnet.connect_output(s2)
        return subnet