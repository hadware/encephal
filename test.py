__author__ = 'marechaux'

from subnet.subnet import *
from subnet.network import *
from datasets.logical_function import *
from execution.training.labeled_database import *
from execution.testing.labeled_database import *
from datasets.encoder.onehot import *
from datasets.MNIST import *
from fill_subnet import *

s = Subnet()

input_size = SocketSize([784])
output_size = SocketSize([10])

FillSubnet.MLP(s,input_size,output_size)

n = Network(s)

db = LogicalFunctionDatabase("xor")
learn_db = MNIST("training")
test_db = MNIST("testing")
encoder = Onehot(output_size)

learning = TrainLabeledDatabase(n, learn_db, encoder, QuadraticError.differential)
testing = TestLabeledDatabase(n, test_db, encoder)

learning.online_learn(10000, 1)

print(testing.test(True))




