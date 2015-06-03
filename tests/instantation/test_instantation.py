__author__ = 'lrx'

import unittest
from nodes.connexion import *
from datasink.datasink import *
from tests.instantation.test_instantation_exception import *

class InstantationTest(unittest.TestCase):

    def setUp(self):
        self.input_datasink = Float2D([1,1])


    def test_nodes_shape(self):
        #Convolutional
        kernel_shape = [1]
        self.assertRaises(IncompatibleShape,ConvolutionalConnexion(self.input_datasink,kernel_shape,ZeroPadding.valid))
        #Pooling
        pooling_shape = [1]
        stride_shape = [1,1]
        self.assertRaises(IncompatibleShape,PoolingConnexion(self.input_datasink,MaxPooling,pooling_shape,stride_shape))
        pooling_shape = [1,1]
        stride_shape = [1]
        self.assertRaises(IncompatibleShape,PoolingConnexion(self.input_datasink,MaxPooling,pooling_shape,stride_shape))