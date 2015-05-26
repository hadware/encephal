__author__ = 'marechaux'

from nodes.subnet import *
from subnet.network import *
from datasets.logical_function import *
from datasets.encoder.onehot import *
from datasets.MNIST import *
from test_options import *

test_subnet = Subnet()
input_size = SocketSize([784])
output_size = SocketSize([10])
FillSubnet.MLP(test_subnet, input_size,output_size)

n = Network(test_subnet)


db = LogicalFunctionDatabase("xor")
learn_db = MNIST("training")
test_db = MNIST("testing")
encoder = Onehot(output_size)

statistic=Statistic(learn_db,test_db,encoder)
#statistic.test(n)
statistic.mean(n,1)








