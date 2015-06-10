__author__ = 'lrx'

from subnet.subnet import *

class SubnetArchitecture():
    '''This class make it possible to design complex association'''

    @staticmethod
    def Sequencing(list_subnet):
        subnet = Subnet()
        len = list_subnet.__len__()
        subnet.create_input(list_subnet[0])
        for i in range(len-1):
            subnet.add_after_node(list_subnet[i],list_subnet[i+1])
        subnet.create_output(list_subnet[len-1])
        return subnet

    @staticmethod
    def Vector(n,generator_subnet,*args):
        subnet = Subnet()
        for i in range(n):
            node_i = generator_subnet(args)
            subnet.create_input(node_i)
            subnet.create_output(node_i)
        return subnet

    @staticmethod
    def Matrix(m,n,generator_subnet,*args):
        subnet = Subnet()
        node_00 = generator_subnet(args)
        subnet.create_input(node_00)
        subnet.create_output(node_00)
        for j in range(n):
            node_0j = generator_subnet(args)
            subnet.connect_input(node_0j,j)
            subnet.create_output(node_0j)
        for i in range(1,m):
            node_i1 = generator_subnet(args)
            subnet.create_input(node_i1)
            subnet.connect_output(node_i1,i)
        for i in range(1,m):
            for j in range(1,n):
                node_ij = generator_subnet(args)
                subnet.connect_input(node_ij,i)
                subnet.connect_output(node_ij,j)
        return subnet
