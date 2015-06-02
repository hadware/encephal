__author__ = 'lrx'

import unittest
from subnet.subnet import *
from nodes.layer import *
from nodes.math_function.math_function import *
from datasink.node_socket import *
from tests.construction_exception import *


class AfterConstructionTest(unittest.TestCase):
    """Test case used to check that after the construction of a subnet, everything is going well """

    def setUp(self):
        """Initialisation des tests."""
        self.test_subnet = Subnet()
        self.test_node_pipe1 = PerceptronLayer(Float1D([1]),Sigmoid)
        self.test_node_pipe2 = PerceptronLayer(Float1D([1]),Sigmoid)

    def test_emptySubnet(self):
        self.assertRaises(EmptySubnetError,self.test_subnet.schedule)

    def test_noInput(self):
        self.test_subnet.create_output(self.test_node_pipe1)
        self.assertRaises(NoInputError,self.test_subnet.schedule)

    def test_noOutput(self):
        self.test_subnet.create_input(self.test_node_pipe1)
        self.assertRaises(NoOutputError,self.test_subnet.schedule)

    def test_subnetPresence(self):
        self.test_subnet.create_input(self.test_node_pipe1)
        self.test_subnet.create_output(self.test_node_pipe2)
        s = Subnet()
        self.test_subnet.nodes.add(s)
        self.assertRaises(SubnetPresenceError,self.test_subnet.schedule)

    def test_noInputSocketForEachNode(self):
        #Notice: self.test_node_pipe2 doesn't have an input_socket
        self.test_subnet.create_input(self.test_node_pipe1)
        self.test_subnet.create_output(self.test_node_pipe2)
        self.assertRaises(NoInputSocketForEachNode,self.test_subnet.schedule)

    """def test_noConvex(self):
        self.test_subnet.create_input(self.test_node_pipe1)
        self.test_subnet.create_output(self.test_node_pipe2)

        socket=Socket(self.test_node_pipe2.input_node_socket.datasink)
        self.test_subnet.sockets.add(socket)
        self.test_node_pipe2.input_node_socket.connect_socket(socket)
        print("here")
        self.assertRaises(NoConvexError,self.test_subnet.schedule)"""