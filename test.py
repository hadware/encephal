__author__ = 'marechaux'

from subnet.network import *
from datasets.logical_function import *
from datasets.encoder.onehot import *
from datasets.MNIST import *
from test_options import *


test_subnet = Subnet()
input_datasink = Float2D([28,28])
output_datasink = Float1D([10])

FillSubnet.MLP2(test_subnet,input_datasink,output_datasink)
#FillSubnet.Dropout(test_subnet,input_datasink,output_datasink,0.8)

n = Network(test_subnet)

db = LogicalFunctionDatabase("xor")
learn_db = MNIST("training")
test_db = MNIST("testing")
encoder = Onehot(output_datasink)

statistic=Statistic(learn_db,test_db,encoder)
statistic.mean(n,1)








