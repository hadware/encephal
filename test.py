__author__ = 'marechaux'

from nodes.subnet import *
from subnet.network import *
from datasets.logical_function import *
from datasets.encoder.onehot import *
from datasets.MNIST import *
from test_options import *


test_subnet = Subnet()
input_datasync = Float2D(28,28)
output_datasync = Float1D(10)
FillSubnet.MLP(test_subnet,input_datasync,output_datasync)

n = Network(test_subnet)


db = LogicalFunctionDatabase("xor")
learn_db = MNIST("training")
test_db = MNIST("testing")
encoder = Onehot(output_datasync)

statistic=Statistic(learn_db,test_db,encoder)
#statistic.test(n)
statistic.mean(n,1)








