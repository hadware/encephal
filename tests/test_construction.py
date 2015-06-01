__author__ = 'lrx'

import unittest
from subnet.subnet import *
from subnet.network import *
from nodes.layer import *
from nodes.math_function.math_function import *




class ConstructionTest(unittest.TestCase):
    """Test case utilisé pour tester la construction de Subnets avec des topologies variées"""

    def setUp(self):
        """Initialisation des tests."""
        self.test_subnet = Subnet()

"""    def tearDown(self):
        Network(self.test_subnet)

    def complete_graph(self):

    def incomplete_graph(self):"""



class ConstructionTestPipeNode(ConstructionTest):

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
