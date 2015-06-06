__author__ = 'lrx'

from subnet.subnet import *

class SubnetArchitecture():

    @staticmethod
    def Vector(generator_subnet,n,input_datasink,output_datasink):
        subnet = Subnet()
        for i in range(n):
            node_i = generator_subnet(input_datasink,output_datasink)
            subnet.create_input(node_i)
            subnet.create_output(node_i)

    @staticmethod
    def Matric(generator_subnet,m,n,input_datasink,output_datasink):
        subnet = Subnet()
        node_00 = generator_subnet(input_datasink,output_datasink)
        subnet.create_input(node_00)
        subnet.create_output(node_00)
        for j in range(n):
            node_0j = generator_subnet(input_datasink,output_datasink)
            subnet.connect_input(node_0j,j)
            subnet.create_output(node_0j)
        for i in range(1,m):
            node_i1 = generator_subnet(input_datasink,output_datasink)
            subnet.create_input(node_i1)
            subnet.connect_output(node_i1,i)
        for i in range(1,m):
            for j in range(1,n):
                node_ij = generator_subnet(input_datasink,output_datasink)
                subnet.connect_input(node_ij,i)
                subnet.connect_output(node_ij,j)

