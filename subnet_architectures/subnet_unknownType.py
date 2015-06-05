__author__ = 'lrx'

from subnet_architectures.subnet_classic import *

"""
Class to test some subnet with Unknown type
"""

class SubnetUnknownType():


    @staticmethod
    def Unknown1(input_datasink,output_datasink):
        subnet = Subnet()
        n = FullConnexion(input_datasink, output_datasink)
        p = PerceptronLayer(Unknown,Sigmoid)
        subnet.add_after_node(n,p)
        subnet.create_input(n)
        subnet.create_output(p)
        return subnet

    @staticmethod
    def Unknown2(input_datasink,output_datasink):
        subnet = Subnet()
        hidden_datasink = Float1D([200])
        n1 = FullConnexion(input_datasink, hidden_datasink)
        p1 = PerceptronLayer(hidden_datasink,Sigmoid)
        n2 = FullConnexion(hidden_datasink, output_datasink)
        p2 = PerceptronLayer(Unknown,Sigmoid)
        subnet.add_after_node(n1,p1)
        subnet.add_after_node(p1,n2)
        subnet.add_after_node(n2,p2)
        subnet.create_input(n1)
        subnet.create_output(p2)
        return subnet