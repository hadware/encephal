__author__ = 'lrx'

import unittest
from subnet.subnet import *
from nodes.layer import *
from nodes.math_function.math_function import *


class InConstructionTest(unittest.TestCase):
    """Test case used to check that during the construction of a subnet, everything is going well """

    def setUp(self):
        """Initialisation des tests."""
        self.test_subnet = Subnet()


class InConstructionTestPipeNode(InConstructionTest):

    def test_input(self):
        datasink = Float1D([10])
        node = PerceptronLayer(datasink,Sigmoid)
        self.test_subnet.create_input(node)
        self.assertIn(node.input_node_socket,self.test_subnet.input_node_sockets)

    def test_output(self):
        datasink = Float1D([10])
        node = PerceptronLayer(datasink,Sigmoid)
        self.test_subnet.create_output(node)
        self.assertIn(node.output_node_socket,self.test_subnet.output_node_sockets)

    def test_nodeConnectOnItself(self):
        datasink = Float1D([10])
        node1 = PerceptronLayer(datasink,Sigmoid)
        self.assertRaises(NodeConnectedToItself,self.test_subnet.connect_nodes(node1,node1))

